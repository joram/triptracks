import React, { Component } from "react";
import Cookies from "js-cookie";
import Route from "./route.js"


export class Routes extends Component {
  constructor(props) {
    super(props);

    // routData[zoom][pubId] = rawData
    this.state = {
      routeData: {},
    };
    this.fetched = [];
  }

  getMoreRoutes(hash, zoom){
    let fetched_key = `${hash}_${zoom}`;
    let url =  "http://localhost:8000/graphql"; //"https://app.triptracks.io/graphql";
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

    fetch(url, {
      method: 'POST',
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
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
      if(this.state.routeData[zoom] === undefined){
        this.state.routeData[zoom] = {}
      }
      if(this.state.routeData[zoom][routeData.pubId] === undefined) {
        this.state.routeData[zoom][routeData.pubId] = routeData
      }
    }
    this.setState(this.state)  // to re-render
    console.log("got", hash, zoom);
  }

  render() {
    return (
      Object.keys(this.state.routeData).map(zoom => {
        return Object.keys(this.state.routeData[zoom]).map(pubId => {
          const data = this.state.routeData[zoom][pubId];
          return <Route data={data} pubId={pubId} key={pubId} zoom={zoom}/>
        })
      })
    )

  }
}


export default Routes;
