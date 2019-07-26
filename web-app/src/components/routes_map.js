import React, {Component} from "react"
import TrailRoute from "./route_map_line.js"
import {GoogleMap, withGoogleMap, withScriptjs} from "react-google-maps"
import Geohash from "latlon-geohash"
import routeStore from '../api-client/routeStore'
import map_zoom_emitter from "../map_zoom_emitter"


let route_components = {};
let default_center =  {lat: 48.4284, lng: -123.3656};
let centered_on_pub_id = null;

class RoutesMapContainer extends Component {
    
    constructor(props) {
        super(props);
        this.map = React.createRef();
        this.state = {};

        routeStore.subscribeGotRoutes(this.gotRoutes.bind(this));
        routeStore.subscribeFinishedGettingRoutes(this.finishedGettingRoutes.bind(this));
    }

    onIdle() {
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
        map_zoom_emitter.zoomChanged(this.map.getZoom());
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
                onRouteSelect={this.props.onRouteSelect}
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

        if(this.props.route !== null){
            if(this._ismounted && centered_on_pub_id !== this.props.route.pubId){
                this.map.fitBounds(this.props.route.bounds);
                centered_on_pub_id = this.props.route.pubId;
            }
        }

        let center = default_center;
        if(this.props.route !== null && this.props.route.bounds !== undefined){
            center = this.props.route.bounds.getCenter();
        }

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