import Geohash from "latlon-geohash"
import auth from "./auth";

let url = "https://api.triptracks.io/graphql";

function log_graphql_errors(query_name, data) {
    if (data.errors !== undefined) {
        data.errors.forEach(function (err) {
            console.log(query_name, " error: ", err.message);
        });
    }
}

function do_graphql_call(query, name, authed=true){
    let body = JSON.stringify({query});
    return fetch(url, {
        method: 'POST',
        mode: "cors",
        headers: auth.getRequestHeaders(),
        body: body
    }).then(r => {
        let data = r.json();
        log_graphql_errors(name, data);
        return data
    });
}

function routes_from_graphql_response(routes, zoom, hasLines=true) {
    let results = [];
    routes.forEach(function (route) {
        if (route === null) {
            console.log(`bad route: ${route}`);
            return
        }

        if (route.lines !== null && hasLines) {
            route.lines = JSON.parse(route[`linesZoom${zoom}`]);
            delete route[`linesZoom${zoom}`];
        }

        if (route.bounds === "{}") {
            console.log(`bad route: ${route.pubId}`);
            return
        }
        // route.bounds = line_utils.string_to_bbox(route.bounds);

        results.push(route);
    });
    return results
}

function hash(ne_lat, ne_lng, sw_lat, sw_lng) {
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

async function get_routes_page(hash, zoom, page) {
    let page_size = 500;
    let query = `
    query get_routes_by_geohash {
      routes(geohash:"${hash}", zoom:${zoom}, page:${page}, pageSize:${page_size}){
        pubId
        bounds
        linesZoom${zoom}
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
        .then(r => {
            return r.json()
        }).then(data => {
            log_graphql_errors("get_routes_page", data);
            let routes = data.data.routes;
            if (routes === null || routes === undefined) {
                console.log("failed to get routes");
                console.log(data);
                return {routes: [], lastPage: true}
            }
            return {
                routes: routes_from_graphql_response(routes, zoom, true),
                lastPage: routes.length !== page_size
            };
        });
}

async function get_routes(hash, zoom) {

    let msg = "";
    let page = 0;
    let routes = [];
    while (true) {
        let data = await get_routes_page(hash, zoom, page);
        routes = routes.concat(data.routes);
        let dt = '' + Date.now();
        msg = `dt:${dt}\npage:${page}\nroutes:${routes.length}\nhash:${hash}\nzoom:${zoom}`;
        if (data.lastPage) {
            break
        }
        page = page + 1
    }
    return {routes: routes, msg: msg};
}

export {hash, do_graphql_call, get_routes_page, get_routes, log_graphql_errors, routes_from_graphql_response}
