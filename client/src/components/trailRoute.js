import React, { Component } from "react";
import {Polyline} from "react-google-maps";
import history from "../history";

export class TrailRoute extends Component {

  constructor(props) {
    super(props);
    this.state = {
      pubId: this.props.pubId,
      lines: {},
      zoom: this.props.zoom,
      bbox: undefined,
    };
    this.addNewData()
  }

  addNewData(){
    let newData = this.props.newData;
    Object.keys(newData).forEach(function(zoom){
      let data = newData[zoom];
      this.addLines(data, zoom);
    }.bind(this))

  }

  addLines(data, zoom){
    let lines = JSON.parse(data.lines);

    let polyLines = [];
    let bounds = new google.maps.LatLngBounds();
    Object.keys(lines).map(i => {
      let coordinates = [];
      Object.keys(lines[i]).map(j => {
        let coord = {lat: lines[i][j][0], lng: lines[i][j][1]};
        coordinates.push(coord);
        if(this.state.bbox === undefined){
          bounds.extend(new google.maps.LatLng(coord));
        }

      });
      polyLines.push(<Polyline
        key={this.state.pubId}
        path={coordinates}
        geodesic={true}
        onClick={this.clicked.bind(this)}
        options={{
          strokeColor: "#ff2527",
          strokeOpacity: 0.75,
          strokeWeight: 2,
        }}
      />);
    });

    if(this.state.bbox === undefined) {
      this.state.bbox = bounds;
    }
    this.state.lines[zoom] = polyLines;
  }

  clicked(){
    history.push('/?route='+this.state.pubId);
  }

  isVisible() {
    let c1 = this.state.bbox.getNorthEast();
    let c2 = this.state.bbox.getSouthWest();

    let map = this.props.map;
    let view_bbox = map.getBounds();
    return view_bbox.contains(c1) || view_bbox.contains(c2);
  }


  render() {
    this.addNewData();

    if(!this.isVisible()){
      return null;
    }

    if(this.state.lines[this.props.zoom] !== undefined) {
      this.curr_zoom = this.props.zoom
    }
    let a = this.state.lines[this.props.zoom];
    if(a !== undefined){
      return a
    }
    a = this.state.lines[this.curr_zoom];
    if(a !== undefined){
      return a
    }
    console.log("had no route for "+this.state.pubId, "at zoom", this.curr_zoom);
    return null;
  }
}


export default TrailRoute;
