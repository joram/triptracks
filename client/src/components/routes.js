import React, { Component } from "react";
import Cookies from "js-cookie";
import TrailRoute from "./trailRoute.js"
import history from "../history";

export class Routes extends Component {
  constructor(props) {
    super(props);

    // routData[zoom][pubId] = rawData
    this.state = {
      routeData: {},
    };
    this.url = "http://127.0.0.1:8000/graphql";
    // this.url = "https://app.triptracks.io/graphql";
    this.fetched = [];
  }

  async getRouteData(hash, pubId){
    if (this.state.routeData.length === 0){
      return await this.getRoute(hash, pubId, 5)
    }

    let zoom = Object.keys(this.state.routeData)[0];
    if(zoom === null){
      return await this.getRoute(hash, pubId, zoom)
    }

    if (this.state.routeData[zoom] === undefined){
      return await this.getRoute(hash, pubId, zoom)
    }

    if (this.state.routeData[zoom][pubId] === undefined){
      return await this.getRoute(hash, pubId, zoom)
    }

    console.log("returning route data I already have");
    return Promise(resolve => {
      return this.state.routeData[zoom][pubId];
    });
  }

  async getBounds(hash, pubId){
    this.getRouteData(hash, pubId).then(
      data => {
        let lines = [];
        console.log("routeData ", data);
        if(data !== undefined && data.lines !== undefined){
          lines = JSON.parse(data.lines);
        }
        let bounds = new google.maps.LatLngBounds();
        Object.keys(lines).map(i => {
          Object.keys(lines[i]).map(j => {
            let lat = lines[i][j][0];
            let lng = lines[i][j][1];
            bounds.extend(new google.maps.LatLng({lat:lat, lng:lng}));
          });
        });
        console.log("bounds calculated for ", lines.length, " vertices");
        return Promise(bounds)
      }
    );
  }

  async getRoute(hash, pubId, zoom){
    let fetched_key = `${hash}_${zoom}`;
    if(this.fetched.indexOf(fetched_key) >= 0){
      console.log("already got");
      return
    }
    this.fetched.push(fetched_key);
    console.log("getting", hash, zoom);

    let query = `
      query {
        route(pubId:"${pubId}", zoom:${zoom}){
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
    .then(data => this.processNewRoute(data, hash, zoom));
  }

  processNewRoute(data, hash, zoom) {
    let routeData = data;
    if(this.state.routeData[zoom] === undefined){
      this.state.routeData[zoom] = {}
    }
    if(this.state.routeData[zoom][routeData.pubId] === undefined) {
      this.state.routeData[zoom][routeData.pubId] = routeData
    }
    return data
  }

  getMoreRoutes(hash, zoom){
    let fetched_key = `${hash}_${zoom}`;
    if(this.fetched.indexOf(fetched_key) >= 0){
      console.log("already got");
      return
    }
    this.fetched.push(fetched_key);
    console.log("getting", hash, zoom);

    let query = `
      query {
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
    .then(data => this.processNewRoutes(data, hash, zoom));
  }

  processNewRoutes(data, hash, zoom){
    if (data.data.routes === undefined){
      return
    }
    for(let i=0; i<data.data.routes.length; i++){
      let routeData = data.data.routes[i];
      this.processNewRoute(routeData, hash, zoom);
      // if(this.state.routeData[zoom] === undefined){
      //   this.state.routeData[zoom] = {}
      // }
      // if(this.state.routeData[zoom][routeData.pubId] === undefined) {
      //   this.state.routeData[zoom][routeData.pubId] = routeData
      // }
    }
    this.setState(this.state);  // to re-render
    console.log("got", hash, zoom);
  }

  render() {
    return (
      Object.keys(this.state.routeData).map(zoom => {
        return Object.keys(this.state.routeData[zoom]).map(pubId => {
          const data = this.state.routeData[zoom][pubId];
          return <TrailRoute data={data} pubId={pubId} key={pubId} zoom={zoom}/>
        })
      })
    )
  }

}


export default Routes;
