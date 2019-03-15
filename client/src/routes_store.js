let EventEmitter = require('events').EventEmitter;
let emitter = new EventEmitter();
let routes_by_hash = {};
let routes_by_pub_id = {};
let url = "https://app.triptracks.io/graphql";
if(window.location.hostname==="localhost") {
  url = "http://127.0.0.1:8000/graphql";
}



function log_graphql_errors(query_name, data){
  if(data.errors !== undefined){
    data.errors.forEach(function(err){
      if(err.message !== "Circular reference detected"){
        console.log(query_name, " error: ", err.message);
      }
    });
  }
}


module.exports = {

  getRoutesByHash2: function(hash, zoom) {
    return routes_by_hash[hash][zoom]
  },

  getRoutesByHash: function(hash, zoom) {

    if(routes_by_hash[hash] !== undefined && routes_by_hash[hash][zoom] !== undefined){
      emitter.emit("got_routes", {hash:hash, zoom:zoom});
      return
    }

    // cache miss
    let query = `
      query get_routes_by_geohash {
        routes(geohash:"${hash}", zoom:${zoom}){
          pubId
          lines
          bounds
          name
        }
      }
    `;
    let body = JSON.stringify({query});
    fetch(url, {
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
      let routes = data.data.routes;
      if(routes === null){
        console.log("failed to get routes")
        return
      }
      if(routes_by_hash[hash] === undefined){
        routes_by_hash[hash] = {};
      }
      routes_by_hash[hash][zoom] = [];
      routes.forEach(function(route){
        route.lines = JSON.parse(route.lines);
        let b = JSON.parse(route.bounds);
        let lat_1 = parseFloat(b[0][0]);
        let lng_1 = parseFloat(b[0][1]);
        let lat_2 = parseFloat(b[1][0]);
        let lng_2 = parseFloat(b[1][1]);
        route.bounds = new google.maps.LatLngBounds();
        route.bounds.extend({lat: lat_1, lng: lng_1});
        route.bounds.extend({lat: lat_2, lng: lng_2});
        route.hash = hash;
        route.zoom = zoom;
        routes_by_hash[hash][zoom].push(route);
      });
      emitter.emit("got_routes", {hash:hash, zoom:zoom})
    });

  },

  getRouteByID2: function(pub_id){
    console.log(pub_id)
    console.log(routes_by_pub_id)
    return routes_by_pub_id[pub_id]
  },

  getRouteByID: function(pub_id) {
    if(routes_by_pub_id[pub_id] !== undefined){
      emitter.emit("got_route", data.route);
      return
    }

    let query = `
      query get_single_route {
        route(pubId:"${pub_id}"){
          pubId
          name
          description
          bounds
        }
      }
    `;

    let body = JSON.stringify({query});
    return fetch(url, {
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
      let route = data.data.route;
      let b = JSON.parse(route.bounds);
      let lat_1 = parseFloat(b[0][0]);
      let lng_1 = parseFloat(b[0][1]);
      let lat_2 = parseFloat(b[1][0]);
      let lng_2 = parseFloat(b[1][1]);
      route.bounds = new google.maps.LatLngBounds();
      route.bounds.extend({lat: lat_1, lng: lng_1});
      route.bounds.extend({lat: lat_2, lng: lng_2});
      routes_by_pub_id[pub_id] = route;
      emitter.emit("got_route", data.data.route);
    });

  },

  subscribeGotRoutes: function(callback) {
    emitter.addListener("got_routes", callback);
  },

  subscribeGotRoute: function(callback) {
    emitter.addListener("got_route", callback);
  },

};