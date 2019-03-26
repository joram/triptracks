import React, { Component } from "react"
import TrailRoute from "./trailRoute.js"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps"
import history from "../history"
import Geohash from "latlon-geohash"
import routeStore from '../routeStore'
import map_zoom_emitter from "../map_zoom_emitter"

class RoutesMapContainer extends Component {

  constructor(props) {
    super(props);
    this.map = React.createRef();
    this.map_center = {lat: 48.4284, lng: -123.3656};
    this.state = {
      route_components: {},
    };
    routeStore.subscribeGotRoutes(this.gotRoutes.bind(this));
    routeStore.subscribeGotRouteByPubId(this.gotRoute.bind(this));
    routeStore.subscribeFinishedGettingRoutes(this.finishedGettingRoutes.bind(this));
  }

  onIdle(){
    if(this.map === undefined || this.map.current === null){
      return
    }
    routeStore.getRoutesByHash(this.hash(this.map_bbox()), this.zoom())
  }

  onZoomChanged(){
    this.state.visible_route_pub_ids = [];
    this.state.visible_routes = [];
    routeStore.getRoutesByHash(this.hash(this.map_bbox()), this.zoom());
    map_zoom_emitter.zoomChanged(this.zoom());
  }

  gotRoutes(data){
    // already got route
    if(this.state.route_components[data.pubId] !== undefined) {
      return
    }

    // new route found
    this.state.route_components[data.pubId] = {
      data: data,
      component: <TrailRoute
        key={"route_"+data.pubId}
        pubId={data.pubId}
        hash={data.hash}
        zoom={this.zoom()}
      />,
    };
  }

  finishedGettingRoutes(data){
    console.log("finished getting routes for the hash");
    this.forceUpdate();
  }

  gotRoute(data) {
    let urlParams = new URLSearchParams(history.location.search);
    let url_pub_id = urlParams.get('route');
    let route = routeStore.getRouteByID2(url_pub_id)
    this.map.fitBounds(route.bounds)
  }

  url_bbox(){
    let urlParams = new URLSearchParams(history.location.search);
    let bbox = urlParams.get('bbox');
    if(bbox===null){
      return null
    }
    let parts = bbox.split(",");
    let n = parseFloat(parts[0]);
    let e = parseFloat(parts[1]);
    let s = parseFloat(parts[2]);
    let w = parseFloat(parts[3]);
    let se = new google.maps.LatLng({lat:s, lng:e});
    let nw = new google.maps.LatLng({lat:n, lng:w});

    let bounds = new google.maps.LatLngBounds();
    bounds.extend(se);
    bounds.extend(nw);
    return bounds
  }

  hash(bounds){
    if(bounds === null){
      bounds = this.map_bbox()
    }
    if(bounds === null) {
      return null
    }

    let ne = bounds.getNorthEast();
    let sw = bounds.getSouthWest();
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

  zoom(){
    if(this.map === undefined || this.map.current === null){
      return 13
    }
    return this.map.getZoom()
  }

  map_bbox(){
    if(this.map === undefined){
      return null
    }
    return this.map.getBounds()
  }

  render(){
    let route_components = [];
    Object.keys(this.state.route_components).forEach( pubId => {
        route_components.push(this.state.route_components[pubId].component);
    });

    return <GoogleMap
        ref={map => {this.map = map}}
        defaultZoom={13}
        defaultCenter={this.map_center}
        defaultOptions={{mapTypeId: 'terrain'}}
        onIdle={this.onIdle.bind(this)}
        onZoomChanged={this.onZoomChanged.bind(this)}>
      >
        {route_components}
      </GoogleMap>
  }


}

const Routes = withScriptjs(withGoogleMap(RoutesMapContainer));

export default Routes;