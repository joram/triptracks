import React, {Component} from "react"
import TrailRoute from "./route_map_line.js"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps"
// import history from "../history"
import Geohash from "latlon-geohash"
import routeStore from '../routeStore'
import map_zoom_emitter from "../map_zoom_emitter"


let route_components = {};
let map_center =  {lat: 48.4284, lng: -123.3656};


class RoutesMapContainer extends Component {
    
    constructor(props) {
        super(props);
        this.map = React.createRef();
        this.has_rendered_once = false;
        this.state = {
            rendered: false,
            has_centered: false,
        };


        let pub_id = this.props.centerOnPubId;
        if(pub_id !== undefined){
            routeStore.getRouteByID(pub_id).then(route => {
                map_center.lat = route.bounds.getCenter().lat();
                map_center.lng = route.bounds.getCenter().lng();
                this.map.fitBounds(route.bounds);
                let state = this.state;
                state.has_centered = true
                this.setState(state)
            });
        }

        routeStore.subscribeGotRoutes(this.gotRoutes.bind(this));
        routeStore.subscribeFinishedGettingRoutes(this.finishedGettingRoutes.bind(this));
    }

    onIdle() {
        if (this.map === undefined || this.map.current === null || !this.has_rendered_once || this.map.getBounds() === null) {
            return
        }
        console.log("hashing", this.map.getBounds())
        let hash = this.hash(this.map.getBounds());
        if (hash.length > 0) {
            routeStore.getRoutesByHash(hash, this.zoom())
        } else {
            let ne = this.map_bbox().getNorthEast();
            let sw = this.map_bbox().getSouthWest();
            let h1 = Geohash.encode(ne.lat(), ne.lng());
            let h2 = Geohash.encode(sw.lat(), sw.lng());
            h1 = h1.substring(0, 1);
            h2 = h2.substring(0, 1);
            if (h1 !== h2) {
                routeStore.getRoutesByHash(h1, this.zoom());
                routeStore.getRoutesByHash(h2, this.zoom());
            } else {
                routeStore.getRoutesByHash('', this.zoom());
            }
        }
    }

    onZoomChanged() {
        let state = this.state;
        state.visible_route_pub_ids = [];
        state.visible_routes = [];
        this.setState(state);
        map_zoom_emitter.zoomChanged(this.zoom());
    }

    gotRoutes(data) {
        // already got route
        if (route_components[data.pubId] !== undefined) {
            return
        }

        // new route found
        route_components[data.pubId] = {
            data: data,
            component: <TrailRoute
                key={`route_${data.pubId}`}
                pubId={data.pubId}
                hash={data.hash}
                zoom={this.zoom()}
            />,
        };
    }

    componentDidMount() {
        this._ismounted = true;
    }

    componentWillUnmount() {
        this._ismounted = false;
    }

    finishedGettingRoutes(data) {
        console.log(`finished getting ${data.num} routes ${data.hash}::${data.zoom}`);
        if(this._ismounted){
            this.forceUpdate()
        }
    }

    hash(bounds) {
        if (bounds === null) {
            return null
        }

        let ne = bounds.getNorthEast();
        let sw = bounds.getSouthWest();
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

    zoom() {
        if (this.map === undefined || this.map === null || this.map.current === null) {
            return 13
        }
        return this.map.getZoom()
    }

    render() {
        let routes = [];
        Object.values(route_components).forEach( data => {
            routes.push(data.component);
        });
        console.log(`rendering ${routes.length} routes for routesMap`);
        console.log(`have ${Object.keys(route_components).length} route_components`)
        // debugger
        let center = map_center;
        console.log("center: ", center);
        this.has_rendered_once = true
        return <GoogleMap
            ref={map => {
                this.map = map
            }}
            defaultZoom={13}
            defaultCenter={center}
            defaultOptions={{mapTypeId: 'terrain'}}
            onIdle={this.onIdle.bind(this)}
            onZoomChanged={this.onZoomChanged.bind(this)}
        >
            {routes}
        </GoogleMap>
    }


}

const RoutesMap = withScriptjs(withGoogleMap(RoutesMapContainer));

export default RoutesMap;