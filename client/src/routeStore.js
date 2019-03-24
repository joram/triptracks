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
    if(route.lines !== null && hasLines){
      route.lines = JSON.parse(route.lines);
    }
    route.bounds = line_utils.string_to_bbox(route.bounds);
    results.push(route);
  });
  return results
}

async function getRoutesPage(hash, zoom, first, skip){
  let query = `
    query get_routes_by_geohash {
      routes(geohash:"${hash}", zoom:${zoom}, first:${first}, skip:${skip}){
        pubId
        bounds
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
    log_graphql_errors("get_routes_page", data);
    let routes = data.data.routes;
    if(routes === null){
      console.log("failed to get routes");
      return []
    }
    return routes_from_graphql_response(data.data.routes, true);
  });
}

module.exports = {

  // getRoutesByHash2: function(hash, zoom) {
  //   if(
  //     routes_by_hash[hash] === undefined ||
  //     routes_by_hash[hash][zoom] === undefined ||
  //     routes_by_hash[hash][zoom] === null)
  //   {
  //     console.log(`sorry, don't have ${hash}::${zoom}`)
  //     return []
  //   }
  //
  //   return routes_by_hash[hash][zoom]
  // },
  //
  getRouteByHashZoomAndPubID: function(hash, zoom, pubId) {
    let key = `${hash}::${zoom}`;
    return routes_by_hash[key].routes[pubId]
  },

  getRoutesByHash: function(hash, zoom) {
    let key = `${hash}::${zoom}`;
    if(routes_by_hash[key] === undefined){
      routes_by_hash[key] = {
        complete: false,
        routes: {},
      }
    }

    if(routes_by_hash[key].complete){
      Object(routes_by_hash[key]["complete"]).keys().forEach((pubId) => {
          emitter.emit("got_routes", {hash:hash, zoom:zoom, pubId:pubId});
          emitter.emit(`got_route_${pubId}`, {hash:hash, zoom:zoom, pubId:pubId});
      });
      emitter.emit("finished_getting_routes");
      return
    }

    function get_page(page, first, skip){
      getRoutesPage(hash,zoom, first, skip).then( routes => {
        routes.forEach((route) => {
          routes_by_hash[key].routes[route.pubId] = route;
          emitter.emit("got_routes", {hash:hash, zoom:zoom, pubId:route.pubId});
          emitter.emit(`got_route_${route.pubId}`, {hash:hash, zoom:zoom, pubId:route.pubId});
        });
        if(routes.length === first){
          get_page(page+1, first, skip+first)
        } else {
          emitter.emit("finished_getting_routes");
        }
      })
    }

    get_page(0,100, 0);
  },

  getRouteByID2: function(pub_id){
    if(routes_by_pub_id[pub_id] === undefined){
      console.log(`sorry, don't have ${pub_id}`)
      return {}
    }

    return routes_by_pub_id[pub_id]
  },

  getRouteByID: function(pub_id) {
    if(pub_id === null){
      return
    }
    if(routes_by_pub_id[pub_id] !== undefined){
      emitter.emit("got_route", pub_id);
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
      emitter.emit("got_route", pub_id);
    });

  },

  getRoutesBySearch2: function(search_text){
    return routes_by_search[search_text];
  },

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

  subscribeGotRoutesWithPubId: function(callback, pubId) {
    emitter.addListener(`got_route_${pubId}`, callback);
  },

  subscribeFinishedGettingRoutes: function(callback) {
    emitter.addListener("finished_getting_routes", callback);
  },

  subscribeGotRouteByPubId: function(callback) {
    emitter.addListener("got_route", callback);
  },

  subscribeGotSearch: function(callback) {
    emitter.addListener("got_search", callback);
  },

};