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
    Object.keys(lines).map(i => {
      let coordinates = [];
      Object.keys(lines[i]).map(j => {
        coordinates.push(
          {lat: lines[i][j][0], lng: lines[i][j][1]}
        )
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

    this.state.lines[zoom] = polyLines;
  }

  clicked(){
    history.push('/?route='+this.state.pubId);
  }

  render() {
    this.addNewData();
    if(this.state.lines[this.props.zoom] !== undefined) {
      this.curr_zoom = this.props.zoom
    }
    return this.state.lines[this.curr_zoom];
  }
}


export default TrailRoute;
