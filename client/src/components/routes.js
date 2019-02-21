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

    let urlParams = new URLSearchParams(history.location.search);
    this.to_center_on = urlParams.get('route');
    this.map = React.createRef();
    this.to_process = {};
    this.routes_at_hash = {};
    this.first = true;
  }

  // async getRouteData(hash, pubId){
  //   if (this.state.routeData.length === 0){
  //     await this.getRoute(hash, pubId, 5)
  //   }
  //
  //   let zoom = Object.keys(this.state.routeData)[0];
  //   if(zoom === null){
  //     await this.getRoute(hash, pubId, zoom)
  //   }
  //
  //   if (
  //     this.state.routeData[zoom] === undefined ||
  //     this.state.routeData[zoom][pubId] === undefined
  //   ){
  //     return await this.getRoute(hash, pubId, zoom);
  //   }
  //
  //   return this.state.routeData[zoom][pubId];
  // }

  async getBounds(hash, pubId){
    let data = await this.getRoute(hash, pubId);
    console.log("data for getBounds", data);
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

  async getRoute(hash, pubId, zoom){
    let fetched_key = `${hash}_${zoom}`;
    this.state.fetched.push(fetched_key);

    let query = `
      query get_single_route {
        route(pubId:"${pubId}"){
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
      this.processNewRoute(data.data.route, hash, zoom);
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
    if (data.data.routes === undefined){
      return
    }

    data.data.routes.forEach(function(route){
      this.processNewRoute(route, hash, zoom);
    }.bind(this));

    this.forceUpdate();
  }

  async centerOnRoute(){
    let urlParams = new URLSearchParams(history.location.search);
    let pubId = urlParams.get('route');
    if(pubId===null){
      return
    }
    let hash = this._currentBboxGeohash();
    let bbox = await this.getBounds(hash, pubId);
    console.log("centering on ",hash, pubId, bbox);
    this.map.fitBounds(bbox);
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

    return (<GoogleMap
      ref={map => {
        this.map = map;
      }}
      defaultZoom={13}
      defaultCenter={{lat: 48.4284, lng: -123.3656}}
      onIdle={this.onIdle.bind(this)}
      defaultOptions={{
        mapTypeId: 'terrain',//google.maps.MapTypeId.TERRAIN,
      }}
    >
      {routes}
    </GoogleMap>);
  }

}


const Routes = withScriptjs(withGoogleMap(RoutesContainer));

export default Routes;

