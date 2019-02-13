import React, { Component } from "react";
import {Polyline} from "react-google-maps";
import history from "../history";

export class TrailRoute extends Component {
  constructor(props) {
    super(props);
    let lines = [];
    if (this.props.data.lines !== undefined){
      lines = JSON.parse(this.props.data.lines);
    }
    this.state = {
      pubId: this.props.pubId,
      lines: lines,
      zoom: this.props.zoom,
    }
  }

  clicked(){
    console.log("map:", this.map)
    history.push('/?route='+this.state.pubId);
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
          onClick={this.clicked.bind(this)}
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


export default TrailRoute;
