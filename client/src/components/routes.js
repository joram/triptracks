import React, { Component } from "react"
import TrailRoute from "./trailRoute.js"
import RouteDetails from "./routeDetails"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps"
import history from "../history"
import Geohash from "latlon-geohash"
let routes = require('../routes_store');

import '@trendmicro/react-sidenav/dist/react-sidenav.css';



export class Routes extends Component {

  constructor(props) {
    super(props);

    this.state = {
      routeData: {},
      routesInGeohash: {},
      currentRoute: null,
      fetched: [],
    };

    history.listen((a, b) => {
      this.updateCurrentRoute();
      this.centerOnRoute();
    });
    console.log("subscribed");
    routes.subscribe(function(route){
      console.log("got something!")
      console.log(route)
    });
    this.updateCurrentRoute();
    this.map = React.createRef();
    this.map_bounds = null;
    this.map_center = {lat: 48.4284, lng: -123.3656};
    this.to_process = {};
    this.routes_at_hash = {};
    this.first = true;
  }

  async getBounds(pubId){
    let data = await this.getRoute(pubId);
    let lines = [];
    if(data !== undefined && data.lines !== undefined){
      lines = JSON.parse(data.lines);
    }
    let bounds = new google.maps.LatLngBounds();
    lines.forEach((line) => {
      line.forEach((coord) => {
        let lat = parseFloat(coord[0]);
        let lng = parseFloat(coord[1]);
        console.log(lat, lng);
        bounds.extend(new google.maps.LatLng({lat:lat, lng:lng}));
      })
    });
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
    return this.map.getZoom()
  }

  map_bbox(){
    if(this.map === undefined){
      return null
    }
    return this.map.getBounds()
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

  updateCurrentRoute(){
    let urlParams = new URLSearchParams(history.location.search);
    let pubId = urlParams.get('route');
    if(pubId === null){
      return
    }

    this.getRoute(pubId).then((route) => {
      this.state.currentRoute = route;
      this.forceUpdate()
    })
  }

  getMoreRoutes(){
    let bbox = this.map_bbox();
    let hash = this.hash(bbox);
    let zoom = this.zoom();
    console.log("getting more routes");
    routes.getRoutesByHash(hash, zoom, false)
  }

  centerOnRoute(){
    let bbox = this.url_bbox();
    if(bbox !== null){
      let c = bbox.getCenter();
      this.map_bounds = bbox;
      this.map_center = {lat: c.lat(), lng: c.lng()};
      this.forceUpdate()
    }
  }

  onIdle(){
    this.getMoreRoutes();
    if(this.to_center_on !== null){
      this.centerOnRoute();
      this.to_center_on = null;
    }
  }

  visibleRoutes(){
    let routes = [];
    let route_pubIds = [];
    let bbox = this.map_bbox();
    let hash = this.hash(bbox);
    if(this.routes_at_hash[hash] === undefined){
      this.routes_at_hash[hash] = [];
    }
    this.routes_at_hash[hash].forEach(function(pubId){
      if(route_pubIds.indexOf(pubId) === -1) {
        let new_data = this.to_process[pubId];
        routes.push(<TrailRoute
          pubId={pubId}
          key={pubId}
          newData={new_data}
          zoom={this.zoom()}
          map={this.map}
        />);
        route_pubIds.push(pubId);
      }
    }.bind(this));
    return routes;
  }

  render(){
    let routes = [];
    if(!this.first){
      routes = this.visibleRoutes();
    }
    this.first = false;

    const styles = {
      width: "100%",
      height: `${window.innerHeight-95}px`
    };

    let container_style = {
      width: "100%",
      marginLeft: "0px",
    };
    if(this.state.currentRoute !== null){
      container_style.marginLeft = "300px";
      container_style.width = `${window.innerWidth-300}px`;
      container_style.height = `${window.innerHeight}px`
    }

    if(this.map_bounds !== null){
      if(this.map !== null && this.map !== undefined){
        this.map.fitBounds(this.map_bounds);
        this.map_bounds = null;
      }
    }
    return <div id="map_and_route_details" style={{styles}} >
      <RouteDetails route={this.state.currentRoute} />
      <RoutesMap
        googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
        loadingElement={<div id="map_loading_element" style={styles} />}
        containerElement={<div id="map_container" style={container_style} />}
        mapElement={<div id="map_element" style={styles} />}

        parent={this}
        routes={routes}
        map_center={this.map_center}
      />
    </div>;
  }

}

export class RoutesMapContainer extends Component {

  constructor(props) {
    super(props);
    this.map = React.createRef();
  }

  onIdle(){
    this.props.parent.onIdle()
  }

  render(){
      return <GoogleMap
          ref={map => {
            this.map = map;
            this.props.parent.map = map;
          }}
          defaultZoom={13}
          onIdle={this.onIdle.bind(this)}
          defaultCenter={this.props.map_center}
          defaultOptions={{mapTypeId: 'terrain'}}
        >
          {this.props.routes}
        </GoogleMap>
  }
}

const RoutesMap = withScriptjs(withGoogleMap(RoutesMapContainer));

export default Routes;

