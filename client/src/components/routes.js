import React, { Component } from "react";
import TrailRoute from "./trailRoute.js"
import RouteDetails from "./routeDetails"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps";
import history from "../history";
import Geohash from "latlon-geohash";


import '@trendmicro/react-sidenav/dist/react-sidenav.css';


function log_graphql_errors(query_name, data){
  if(data.errors !== undefined){
    data.errors.forEach(function(err){
      console.log(query_name, " error: ", err.message);
    });
  }
}

export class Routes extends Component {

  constructor(props) {
    super(props);

    this.state = {
      routeData: {},
      routesInGeohash: {},
      currentRoute: null,
      fetched: [],
    };
    this.url = "https://app.triptracks.io/graphql";
    if(window.location.hostname==="localhost"){
      this.url = "http://127.0.0.1:8000/graphql";
    }

    history.listen((a, b) => {
      this.updateCurrentRoute();
      this.centerOnRoute();
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
    let num_verts = 0;
    let bounds = new google.maps.LatLngBounds();
    Object.keys(lines).map(i => {
      Object.keys(lines[i]).map(j => {
        let lat = lines[i][j][0];
        let lng = lines[i][j][1];
        num_verts += 1;
        bounds.extend(new google.maps.LatLng({lat:lat, lng:lng}));
      });
    });
    return bounds
  }

  async getRoute(pubId){
    console.log("getting route "+pubId);
    let query = `
      query get_single_route {
        route(pubId:"${pubId}"){
          pubId
          name
          description
          lines
        }
      }
    `;

    let body = JSON.stringify({query});
    return fetch(this.url, {
      method: 'POST',
      mode: "cors",
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: body
    })
    .then(r => r.json())
    .then(data => {
      log_graphql_errors("get_single_route", data);
      return data.data.route;
    });
  }

  hash(){
    let bounds = this.map.getBounds();
    if(bounds === null){
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

  bbox(){
    let urlParams = new URLSearchParams(history.location.search);
    let bbox = urlParams.get('bbox');
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

  processNewRoute(route, hash, zoom) {
    if(this.routes_at_hash[hash] === undefined){
      this.routes_at_hash[hash] = [];
    }
    if(this.to_process[route.pubId] === undefined){
      this.to_process[route.pubId] = {};
    }
    this.to_process[route.pubId][zoom] = route;
    this.routes_at_hash[hash].push(route.pubId);
  }

  getMoreRoutes(hash, zoom){
    let fetched_key = `${hash}_${zoom}`;
    if(this.state.fetched.indexOf(fetched_key) !== -1){
      this.forceUpdate();
      return
    }
    this.state.fetched.push(fetched_key);

    let query = `
      query get_more_routes {
        routes(geohash:"${hash}", zoom:${zoom}){
          pubId
          lines
        }
      }
    `;

    let body = JSON.stringify({query});
    fetch(this.url, {
      method: 'POST',
      mode: "cors",
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: body
    })
    .then(r => r.json())
    .then(data => {
      log_graphql_errors("get_more_routes", data);
      this.processNewRoutes(data, hash, zoom)
    });
  }

  processNewRoutes(data, hash, zoom){
    if (data.data === undefined || data.data.routes === null){
      return
    }

    data.data.routes.forEach(function(route){
      this.processNewRoute(route, hash, zoom);
    }.bind(this));

    this.forceUpdate();
  }

  centerOnRoute(){
    let c = this.bbox().getCenter();
    this.map_bounds = this.bbox();
    this.map_center = {lat: c.lat(), lng: c.lng()};
    this.forceUpdate()
  }

  onIdle(){
    this.getMoreRoutes(this.hash(), this.map.getZoom());
    if(this.to_center_on !== null){
      this.centerOnRoute();
      this.to_center_on = null;
    }
  }

  visibleRoutes(){
    let routes = [];
    let route_pubIds = [];
    if(this.routes_at_hash[this.hash()] === undefined){
      this.routes_at_hash[this.hash()] = [];
    }
    this.routes_at_hash[this.hash()].forEach(function(pubId){
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
      height: `${window.innerHeight-100}px`
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

