import React, { Component } from "react";
import {Polyline} from "react-google-maps";
import history from "../history";

export class TrailRoute extends Component {

  constructor(props) {
    super(props);
    this.state = {
      pubId: this.props.pubId,
      zoom: this.props.zoom,
      bounds: this.props.bounds,
      lines: {},
    };
  }

  addLines(){
    if(this.state.lines[this.props.data.zoom] !== undefined){
      return
    }

    let lines = this.props.data.lines;

    let polyLines = [];
    if(lines === null){
      return
    }

    lines.forEach( (line) => {
      if(line === null){
        return
      }

      let coordinates = [];
      line.forEach( (coord) => {
        coordinates.push({lat: coord[0], lng: coord[1]});
      });

      polyLines.push(<Polyline
        key={"line_"+polyLines.length+1+"_"+this.state.pubId}
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
    this.state.lines[this.props.data.zoom] = polyLines;
  }

  clicked(){
    history.push(`/?route=${this.state.pubId}&bbox=${this.state.bounds.toUrlValue()}`);
  }

  render() {
    this.addLines()
    return this.state.lines[this.props.data.zoom];
  }
}


export default TrailRoute;
