import React, { Component } from "react";
import {Polyline} from "react-google-maps";

export class Route extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pubId: this.props.pubId,
      lines: JSON.parse(this.props.data.lines),
      zoom: this.props.zoom,
    }
  }

  render() {
    return (
      Object.keys(this.state.lines).map(i => {
        let coordinates = [];
        Object.keys(this.state.lines[i]).map(j => { coordinates.push(
          {lat:this.state.lines[i][j][0], lng:this.state.lines[i][j][1]}
        )});
        return <Polyline
          key={this.state.pubId}
          path={coordinates}
          geodesic={true}
          options={{
            strokeColor: "#ff2527",
            strokeOpacity: 0.75,
            strokeWeight: 2,
          }}
        />
      })
    )
  }
}


export default Route;
