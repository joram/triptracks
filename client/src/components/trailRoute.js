import React, { Component } from "react";
import {Polyline} from "react-google-maps";
import history from "../history";
import routeStore from "../routeStore";
import map_zoom_emitter from "../map_zoom_emitter";

export class TrailRoute extends Component {

  constructor(props) {
    super(props);
    this.pubId = this.props.pubId;
    this.state = {
      lines: {},  // key'ed on zoom
      current_zoom: this.props.zoom,
      bounds: [],
      showing_zoom: -1,
    };
    routeStore.subscribeGotRoutesWithPubId(this.moreDataForThisRoute.bind(this), this.pubId);
    map_zoom_emitter.subscribeZoomChange(this.zoomChanged.bind(this));
    this.addLines(this.props.hash, this.props.zoom);
  }

  zoomChanged(data){
    this.state.current_zoom = data.zoom;
    if(this.state.showing_zoom !== data.zoom){
      this.forceUpdate()
    }
  }

  moreDataForThisRoute(data) {
    this.addLines(data.hash, data.zoom);
  }

  addLines(hash, zoom){
    if(this.state.lines[zoom] !== undefined){
      return
    }

    let polyLines = [];
    let route = routeStore.getRouteByHashZoomAndPubID(hash, zoom, this.pubId);
    if(route === undefined) {
      return
    }
    this.state.bounds = route.bounds;
    if(route.lines === null){
      return
    }
    route.lines.forEach( (line) => {
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
    this.state.lines[zoom] = polyLines;
  }

  clicked(){
    history.push(`/?route=${this.pubId}&bbox=${this.state.bounds.toUrlValue()}`);
  }

  render() {
    if(this.state.showing_zoom === this.state.current_zoom){
      return null
    }

    let component = this.state.lines[this.state.current_zoom];
    if(component === undefined){
      let old_component = this.state.lines[this.state.showing_zoom];
      if(old_component !== undefined){
        return old_component
      }
      return null
    }

    this.state.showing_zoom = this.state.current_zoom;
    return component
  }
}


export default TrailRoute;
