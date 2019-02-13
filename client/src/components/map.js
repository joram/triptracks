import React, { Component } from "react";
import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
} from "react-google-maps";
import Routes from "./routes.js"
import Geohash from "latlon-geohash";
import history from "../history";

export class MapContainer extends Component {

  constructor(props) {
    super(props);
    this.map = React.createRef();
    this.routes = React.createRef();
    history.listen((location, action) => {
      this.centerOnRoute()
    });
    let urlParams = new URLSearchParams(history.location.search);
    this.toCenterOn = urlParams.get('route');
  }

  centerOnRoute(){
      let urlParams = new URLSearchParams(history.location.search);
      let pubId = urlParams.get('route');
      if(pubId===null){
        return
      }
      let hash = this._currentBboxGeohash();
      let bbox = this.routes.current.getBounds(hash, pubId);
      console.log("centering on ", hash, bbox);
      this.map.fitBounds(hash, bbox);
  }

  _currentBboxGeohash() {
    let ne = this.map.getBounds().getNorthEast();
    let sw = this.map.getBounds().getSouthWest();
    let h1 = Geohash.encode(ne.lat(), ne.lng());
    let h2 = Geohash.encode(sw.lat(), sw.lng());

    let h = "";
    for (let i = 0; i < h1.length; i++) {
      if (h1[i] !== h2[i])
        break;
      h += h1[i]
    }
    return h
  }


  onIdle(){
    this.routes.current.getMoreRoutes(this._currentBboxGeohash(), this.map.getZoom())
    if(this.toCenterOn !== null){
      console.log("centering on ", this.toCenterOn);
      this.centerOnRoute();
      this.toCenterOn = null;
    }
  }

  render() {
    return (<GoogleMap
      ref={map => {this.map = map;}}
      defaultZoom={13}
      defaultCenter={{lat: 48.4284, lng: -123.3656}}
      onIdle={this.onIdle.bind(this)}
    >
      <Routes ref={ this.routes } />
    </GoogleMap>)
  }
}

const Map = withScriptjs(withGoogleMap(MapContainer));
export default Map