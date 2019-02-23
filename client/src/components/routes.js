import React, { Component } from "react";
import TrailRoute from "./trailRoute.js"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps";
import history from "../history";
import Geohash from "latlon-geohash";

function log_graphql_errors(data){
  if(data.errors !== undefined){
    data.errors.forEach(function(err){
      console.log("error: ",err.message);
    });
  }
}

export class RoutesContainer extends Component {

  constructor(props) {
    super(props);

    // routData[zoom][pubId] = rawData
    this.state = {
      routeData: {},
      routesInGeohash: {},
      fetched: [],
    };
    this.url = "https://app.triptracks.io/graphql";
    if(window.location.hostname==="localhost"){
      this.url = "http://127.0.0.1:8000/graphql";
    }

    history.listen((location, action) => {
      this.centerOnRoute()
    });

    this.map_center = {lat: 48.4284, lng: -123.3656};
    let urlParams = new URLSearchParams(history.location.search);
    let bbox = urlParams.get('bbox');
    if(bbox !== null){
      let parts = bbox.split(",");
      let n = parseFloat(parts[0]);
      let e = parseFloat(parts[1]);
      let s = parseFloat(parts[2]);
      let w = parseFloat(parts[3]);
      let center_lat = (e+w)/2;
      let center_lng = (n+s)/2;
      this.map_center = {lat: center_lat, lng: center_lng};
    }

    this.map = React.createRef();
    this.to_process = {};
    this.routes_at_hash = {};
    this.first = true;
  }


  async getBounds(hash, pubId){
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

    let query = `
      query get_single_route {
        route(pubId:"${pubId}"){
          pubId
          name
          description
          lines
          owner{
            pubId
          }
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
      log_graphql_errors(data);
      return data.data.route;
    });
  }

  hash() {
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

  zoom(){
    return this.map.getZoom()
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
          name
          lines
          owner{
            pubId
          }
        }
      }
    `;

    let body = JSON.stringify({query});
    console.log(`getting more routes ${hash} ${zoom}`);
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
      log_graphql_errors(data);
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

  async centerOnRoute(){
    console.log("centering");
    let urlParams = new URLSearchParams(history.location.search);
    let pubId = urlParams.get('route');
    if(pubId !== null){
      let hash = this._currentBboxGeohash();
      let bbox = await this.getBounds(hash, pubId);
      console.log("centering on ",hash, pubId, bbox);
      this.map.fitBounds(bbox);
    }

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
    this.getMoreRoutes(this._currentBboxGeohash(), this.map.getZoom())
    if(this.to_center_on !== null){
      this.centerOnRoute();
      this.to_center_on = null;
    }
  }

  render() {
    let routes = [];
    let route_pubIds = [];
    if(!this.first){
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
    }

    this.first = false;

    return <GoogleMap
        ref={map => {
          this.map = map;
        }}
        defaultZoom={13}
        defaultCenter={this.map_center}
        onIdle={this.onIdle.bind(this)}
        containerElement={<div style={{width: "100%", marginLeft: 0 }} />}
        defaultOptions={{
          mapTypeId: 'terrain',//google.maps.MapTypeId.TERRAIN,
        }}
      >
        {routes}
      </GoogleMap>;
  }

}


const Routes = withScriptjs(withGoogleMap(RoutesContainer));

export default Routes;

