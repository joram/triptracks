import React, { Component } from "react";
import {Polyline} from "react-google-maps";
import history from "../history";

export class TrailRoute extends Component {

  constructor(props) {
    super(props);
    this.state = {
      pubId: this.props.pubId,
      zoom: this.props.zoom,
      bbox: this.props.bbox,
      lines: {},
    };
  }

  addLines(){
    let zoom = this.props.zoom;
    let lines = this.props.data.lines;

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
    console.log(`clicked on ${this.state.pubId}`);
    history.push(`/?route=${this.state.pubId}&bbox=${this.state.bbox.toUrlValue()}`);
  }


  render() {
    this.addLines()

    if(this.state.lines[this.props.zoom] !== undefined) {
      this.curr_zoom = this.props.zoom
    }
    let a = this.state.lines[this.props.zoom];
    if(a !== undefined){
      this.previous_zoom = this.props.zoom;
      return a
    }
    a = this.state.lines[this.previous_zoom];
    if(a !== undefined){
      return a
    }
    console.log("had no route for "+this.state.pubId, "at zoom", this.zoom);
    return null;
  }
}


export default TrailRoute;
