import line_utils from './line_utils'
import auth from"./auth"
import {do_graphql_call, log_graphql_errors, routes_from_graphql_response} from "./utils";

let EventEmitter = require('events').EventEmitter;
let emitter = new EventEmitter();

let routes_by_hash = {};
let routes_by_pub_id = {};
let routes_by_search = {};


async function getRoutesPage(hash, zoom, page) {
    let page_size = 500;
    let query = `
        query get_routes_by_geohash {
          routes(geohash:"${hash}", zoom:${zoom}, page:${page}, pageSize:${page_size}){
            pubId
            bounds
            linesZoom${zoom}
            sourceImageUrl
          }
        }
        `;
    return do_graphql_call(query, "get routes page", false).then(data => {
        log_graphql_errors("get_routes_page", data);
        let routes = data.data.routes;
        if (routes === null) {
            return {routes: [], lastPage: true}
        }
        return {
            routes: routes_from_graphql_response(data.data.routes, zoom, true),
            lastPage: routes.length !== page_size
        };
    });
}


export default {

    isLoggedIn: function(){
        return auth.isAuthed()
    },

    getOrCreateUser: function (googleCreds) {
        googleCreds = JSON.stringify({googleCreds}).replace(/"/g, '\\"');
        let query = `mutation {
          getOrCreateUser(googleCredentials: "${googleCreds}"){
            ok
            user {
              pubId
            }
            sessionToken {
              pubId,
              sessionKey
            }
          }
        }`;

        do_graphql_call(query, "get-or-create-user").then(data => {
            let sessionToken = data.data.getOrCreateUser.sessionToken.sessionKey;
            auth.setSessionToken(sessionToken);
            emitter.emit("got_user");
        });

    },

    getRouteByHashZoomAndPubID: function (hash, zoom, pubId) {
        let key = `${hash}::${zoom}`;
        if (routes_by_hash[key] === undefined) {
            return undefined
        }
        return routes_by_hash[key].routes[pubId]
    },

    getRoutesByHash: function (hash, zoom) {
        let key = `${hash}::${zoom}`;
        if (routes_by_hash[key] !== undefined) {
            return
        }

        routes_by_hash[key] = {
            complete: false,
            routes: {},
        };


        let routes_got = 0;

        function get_page(page) {
            getRoutesPage(hash, zoom, page).then(data => {
                data.routes.forEach((route) => {
                    routes_by_hash[key].routes[route.pubId] = route;
                    emitter.emit("got_routes", {hash: hash, zoom: zoom, pubId: route.pubId});
                    emitter.emit(`got_route_${route.pubId}`, {hash: hash, zoom: zoom, pubId: route.pubId});
                    routes_got += 1;
                });
                if (!data.lastPage) {
                    get_page(page + 1)
                } else {
                    emitter.emit(`finished_getting_routes`, {hash: hash, zoom: zoom, num: routes_got});
                }
            })
        }

        get_page(0);
    },

    getRouteByID2: function (pub_id) {
        if (routes_by_pub_id[pub_id] === undefined) {
            console.log(`sorry, don't have ${pub_id}`);
            return {}
        }

        return routes_by_pub_id[pub_id]
    },

    getRouteByID: async function (pub_id) {

        if (pub_id === null) {
            console.log("dont have", pub_id);
            return null
        }
        if (routes_by_pub_id[pub_id] !== undefined) {
            console.log("have:", routes_by_pub_id[pub_id]);
            emitter.emit("got_route", pub_id);
            return routes_by_pub_id[pub_id]
        }

        let query = `
          query get_single_route {
            route(pubId:"${pub_id}", zoom:15){
              pubId
              name
              bounds
              description
              sourceImageUrl
            }
          }
        `;
        return do_graphql_call(query, "get_single_route").then(data => {
            let route = data.data.route;
            if (route === null) {
                return null
            }
            if (route.bounds === undefined) {
                return null
            }
            route.bounds = line_utils.string_to_bbox(route.bounds);
            routes_by_pub_id[pub_id] = route;
            emitter.emit("got_route", pub_id);
            return route

        });
    },

    getRoutesBySearch2: function (search_text) {
        return routes_by_search[search_text];
    },

    getRoutesBySearch: function (search_text) {
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
        return do_graphql_call(query, "route_search").then(data => {
            routes_by_search[search_text] = routes_from_graphql_response(data.data.routesSearch, null, false);
            emitter.emit("got_search", {search_text: search_text});
            return routes_by_search[search_text];
        });
    },

    getBucketListRoutes: function () {
        let query = `
          query bucket_list_routes {
            bucketListRoutes{
              pubId
              name
              description
              bounds
              sourceImageUrl
            }
          }
        `;
        return do_graphql_call(query, "bucket_list_routes").then(data => {
            return routes_from_graphql_response(data.data.bucketListRoutes, null, false)
        });
    },

    getStravaActivities: function () {
        let query = "query owner_routes { ownerRoutes {pubId, name, description, bounds, sourceImageUrl} }";
        return do_graphql_call(query, "owner_routes").then(data => {
            return routes_from_graphql_response(data.data.ownerRoutes, null, false);
        });
    },

    addToBucketList: function (route_pub_id) {
        let query = `mutation { addBucketListRoute(routePubId: "${route_pub_id}"){ok} }`;
        return do_graphql_call(query, "add_to_bucket_list");
    },

    removeFromBucketList: function (route_pub_id) {
        let query = `mutation { removeBucketListRoute(routePubId: "${route_pub_id}"){ok} }`;
        return do_graphql_call(query, "remove_from_bucket_list");
    },

    removeOwnedRoute: function (route_pub_id) {
        let query = `mutation { removeOwnedRoute(routePubId: "${route_pub_id}"){ok} }`;
        return do_graphql_call(query, "remove_from_bucket_list");
    },

    createOrUpdatePlan: function (pub_id, name, summary, route_pub_id, packing_list_pub_id, start_datetime, end_datetime) {
        let start = new Date().getTime() / 1000;
        let end = new Date().getTime() / 1000;
        let query = `mutation { createOrUpdateTripPlan(
            pubId:"${pub_id}",
            name:"${name}",
            summary:"${summary}",
            routePubId:"${route_pub_id}",
            packingListPubId:"${packing_list_pub_id}",
            startDatetime:${start},
            endDatetime:${end},
        ){ok, pubId} }`;
        console.log(query);
        return do_graphql_call(query, "create_or_update_plan");
    },

    getTripPlans: function () {
        let query = `query trip_plans {
            tripPlans {
                pubId,
                name,
                summary,
                startDatetime,
                endDatetime,
                route {
                    pubId,
                    name,
                    description,
                    bounds,
                    sourceImageUrl,
                },
            }
        }`;
        return do_graphql_call(query, "trip_plans").then(data => {
            log_graphql_errors("trip_plans", data);
            return data.data.tripPlans;
        });
    },

    subscribeGotRoutes: function (callback) {
        emitter.addListener("got_routes", callback);
    },

    subscribeGotRoutesWithPubId: function (callback, pubId) {
        emitter.addListener(`got_route_${pubId}`, callback);
    },

    subscribeFinishedGettingRoutes: function (callback) {
        emitter.addListener("finished_getting_routes", callback);
    },

    subscribeGotRouteByPubId: function (callback) {
        emitter.addListener("got_route", callback);
    },

    subscribeGotSearch: function (callback) {
        emitter.addListener("got_search", callback);
    },

    subscribeGotUser: function (callback) {
        emitter.addListener("got_user", callback);
    },

};