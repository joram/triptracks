import React, { Component } from "react"
import TrailRoute from "./trailRoute.js"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps"
import history from "../history"
import Geohash from "latlon-geohash"
import routes_store from '../routes_store'


export class RoutesMapContainer extends Component {

  constructor(props) {
    super(props);
    this.map = React.createRef();
    this.map_center = {lat: 48.4284, lng: -123.3656};
    this.state = {visible_routes: []}
    routes_store.subscribeGotRoutes(this.gotRoutes.bind(this));
    routes_store.subscribeGotRoute(this.gotRoute.bind(this));
  }

  onIdle(){
    this.getMoreRoutes();
  }

  getMoreRoutes(){
    let bbox = this.map_bbox();
    let hash = this.hash(bbox);
    let zoom = this.zoom();
    routes_store.getRoutesByHash(hash, zoom, false)
  }

  gotRoutes(data){
    let visible_routes = [];
    let visible_route_pub_ids = [];
    let zoom = this.zoom();
    let hash = this.hash(this.map_bbox());
    let routes_in_hash = routes_store.getRoutesByHash2(hash, zoom);
    routes_in_hash.forEach( (route) => {
      if(visible_route_pub_ids.indexOf(route.pubId) !== -1){
        return
      }
      visible_route_pub_ids.push(route.pubId)
      if (route.bounds) {
        if (this.map_bbox().intersects(route.bounds)) {
          visible_routes.push(<TrailRoute
            key={route.pubId}
            pubId={route.pubId}
            zoom={zoom}
            data={route}
          />)
        }
      }
    });
    this.setState({visible_routes:visible_routes})
  }

  gotRoute(data) {
    let urlParams = new URLSearchParams(history.location.search);
    let url_pub_id = urlParams.get('route');
    let route = routes_store.getRouteByID2(url_pub_id)
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
    if(this.map === undefined){
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
    return <GoogleMap
        ref={map => {this.map = map}}
        defaultZoom={13}
        defaultCenter={this.map_center}
        defaultOptions={{mapTypeId: 'terrain'}}
        onIdle={this.onIdle.bind(this)}
      >
        {this.state.visible_routes}
      </GoogleMap>
  }
}


const Routes = withScriptjs(withGoogleMap(RoutesMapContainer));

export default Routes;

