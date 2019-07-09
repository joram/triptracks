import {Polyline} from "react-native-maps";
import React from "react";
import Geohash from "latlon-geohash"
let url = "https://app.triptracks.io/graphql";

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
    if(route === null){
      console.log(`bad route: ${route}`);
      return
    }

    if(route.lines !== null && hasLines){
      route.lines = JSON.parse(route.lines);
    }

    if(route.bounds === "{}"){
      console.log(`bad route: ${route.pubId}`);
      return
    }
    // route.bounds = line_utils.string_to_bbox(route.bounds);

    results.push(route);
  });
  return results
}

function hash(ne_lat, ne_lng, sw_lat, sw_lng){
  let h1 = Geohash.encode(ne_lat, ne_lng);
  let h2 = Geohash.encode(sw_lat, sw_lng);

  let h = "";
  for (let i = 0; i < h1.length; i++) {
    if (h1[i] !== h2[i])
      break;
    h += h1[i]
  }
  return h
}

async function get_routes_page(hash, zoom, page){
  let page_size = 500;
  let query = `
    query get_routes_by_geohash {
      routes(geohash:"${hash}", zoom:${zoom}, page:${page}, pageSize:${page_size}){
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
      console.log(data);
      return {routes:[], lastPage: true}
    }
    return {
      routes:routes_from_graphql_response(data.data.routes, true),
      lastPage: routes.length !== page_size
    };
  });
}

async function get_routes(hash, zoom){

    let routes = [];
    function get_page(page){
      return get_routes_page(hash,zoom, page).then( data => {
        routes = routes.concat(data.routes);
        if(!data.lastPage){
          let more_routes = get_page(page+1);
          routes = routes.concat(more_routes);
        }
        return routes;
      })
    }

    return get_page(0);

}

function lines(){

    return [<Polyline
		coordinates={[
			{ latitude: 37.8025259, longitude: -122.4351431 },
			{ latitude: 37.7896386, longitude: -122.421646 },
			{ latitude: 37.7665248, longitude: -122.4161628 },
			{ latitude: 37.7734153, longitude: -122.4577787 },
			{ latitude: 37.7948605, longitude: -122.4596065 },
			{ latitude: 37.8025259, longitude: -122.4351431 }
		]}
		strokeColor="#000" // fallback for when `strokeColors` is not supported by the map-provider
		strokeColors={[
			'#7F0000',
			'#00000000', // no color, creates a "long" gradient between the previous and next coordinate
			'#B24112',
			'#E5845C',
			'#238C23',
			'#7F0000'
		]}
		strokeWidth={6}
	/>]
}

export { hash, get_routes_page, get_routes }
