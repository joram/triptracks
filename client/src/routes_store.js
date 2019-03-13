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
      console.log(query_name, " error: ", err.message);
    });
  }
}


module.exports = {

  getRoutesByHash: function(hash, zoom, emit_cached) {

    if(routes_by_hash[hash] !== undefined && routes_by_hash[hash][zoom] !== undefined){
      if(emit_cached){
        routes_by_hash[hash][zoom].forEach(function(route) {
          if (routes_by_hash[hash] === undefined) {
            routes_by_hash[hash] = {}
          }
          route.hash = hash;
          route.zoom = zoom;
          emitter.emit("route_by_hash", route);
        })
      }
      return
    }

    // cache miss
    let query = `
      query get_routes_by_geohash {
        routes(geohash:"${hash}", zoom:${zoom}){
          pubId
          lines
          bounds
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
      if(routes_by_hash[hash] === undefined){
        routes_by_hash[hash]={}
      }
      routes_by_hash[hash][zoom] = routes;
      routes.forEach(function(route){
        route.lines = JSON.parse(route.lines);
        route.hash = hash;
        route.zoom = zoom;
        emitter.emit("route", route)
      });
    });

  },

  getRouteByID: function(pub_id) {
    if(routes_by_pub_id[pub_id] !== undefined){
      emitter.emit("route", data.route);
      return
    }

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
      console.log(data);
      routes_by_pub_id[pub_id] = data.route
      emitter.emit("route", data.route)
    });

  },

  subscribe: function(callback) {
    emitter.addListener("route", callback);
  },

  unsubscribe: function(callback) {
    emitter.removeListener("route", callback);
  },
};