import line_utils from './line_utils'

let EventEmitter = require('events').EventEmitter;
let emitter = new EventEmitter();

let url = "https://app.triptracks.io/graphql";
if(window.location.hostname==="localhost") {
  url = "http://127.0.0.1:8000/graphql";
}

let routes_by_hash = {};
let routes_by_pub_id = {};
let routes_by_search = {};


function log_graphql_errors(query_name, data){
  if(data.errors !== undefined){
    data.errors.forEach(function(err){
      console.log(query_name, " error: ", err.message);
    });
  }
}

function routes_from_graphql_response(routes, hasLines){
  let results = [];
  routes.forEach(function(route){
    if(route.lines === null){
      return
    }
    if(hasLines){
      route.lines = JSON.parse(route.lines);
    }
    route.bounds = line_utils.string_to_bbox(route.bounds);
    results.push(route);
  });
  return results
}

module.exports = {

  getRoutesByHash2: function(hash, zoom) {
    return routes_by_hash[hash][zoom]
  },

  getRoutesByHash: function(hash, zoom) {

    if(
      routes_by_hash[hash] !== undefined &&
      routes_by_hash[hash][zoom] !== undefined &&
      routes_by_hash[hash][zoom] !== null)
    {
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
      console.log(data);
      log_graphql_errors("get_more_routes", data);
      let routes = data.data.routes;
      if(routes === null){
        console.log("failed to get routes");
        return
      }
      if(routes_by_hash[hash] === undefined){
        routes_by_hash[hash] = {};
      }
      routes_by_hash[hash][zoom] = routes_from_graphql_response(data.data.routes, true);
      emitter.emit("got_routes", {hash:hash, zoom:zoom})
    });

  },

  getRouteByID2: function(pub_id){
    return routes_by_pub_id[pub_id]
  },

  getRouteByID: function(pub_id) {
    if(pub_id === null){
      return
    }
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
          sourceImageUrl
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
      if(route===null){
        return
      }
      route.bounds = line_utils.string_to_bbox(route.bounds);
      routes_by_pub_id[pub_id] = route;
      emitter.emit("got_route", data.data.route);
    });

  },

  getRoutesBySearch2: function(search_text){
    return routes_by_search[search_text];
  },

  // TODO, make this work with route_search.js
  getRoutesBySearch: function(search_text) {
    let query = `
      query route_search {
        routesSearch(searchText:"${search_text}"){
          pubId
          name
          description
          bounds
          sourceImageUrl
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
      log_graphql_errors("route_search", data);
      routes_by_search[search_text] = routes_from_graphql_response(data.data.routesSearch, false);
      emitter.emit("got_search", {search_text:search_text});
    });


  },
  subscribeGotRoutes: function(callback) {
    emitter.addListener("got_routes", callback);
  },

  subscribeGotRoute: function(callback) {
    emitter.addListener("got_route", callback);
  },

  subscribeGotSearch: function(callback) {
    emitter.addListener("got_search", callback);
  },

};