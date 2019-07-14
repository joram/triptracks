import React, { Component } from 'react';
import MapView, { Polyline } from 'react-native-maps'
import * as Location from 'expo-location';
import { Text, View } from 'react-native';
import { hash, get_routes } from './utils';


class TriptracksApp extends Component {

    constructor(props){
        super(props);
        this.map = null;
        this.current_hash = null;
        this._routes_cache = {};
        this.state = {
            msg: "Hello World",
            got_routes: false,
            routes: [],
            mounted: false,
        }
    }

    componentDidMount() {
        let state = this.state;
        state.mounted = true;
        this.setState(state);

        // monitor location
        let options = { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 };
        Location.requestPermissionsAsync();
        Location.hasServicesEnabledAsync().then(enabled => {
            if(enabled){
                Location.watchPositionAsync(options, this.positionUpdated.bind(this));
                Location.getCurrentPositionAsync(options).then(position => {
                    this.positionUpdated(position);
                });
                return
            }

            Location.requestPermissionsAsync().then(() => {
                Location.watchPositionAsync(options, this.positionUpdated.bind(this))
            })
        });
    }

    positionUpdated(position){
        const { latitude, longitude } = position.coords;
        let region = {
            latitude: latitude,
            longitude: longitude,
            latitudeDelta: 0.004,
            longitudeDelta: 0.004,
        };

        if(this.map !== null && !this.state.got_routes){
            this.map.animateCamera({latitude, longitude});
            this.map.animateToRegion(region);
        } else {
            // if(this.state.mounted){
            // this.forceUpdate()
            //
            // }
        }

    }

    async getCachedRoutes(h, zoom){
        let key = `${h}_${zoom}`;
        let routes = this._routes_cache[key];
        if(routes !== undefined){ return routes}
        return await get_routes(h, zoom).then(data => {
            this._routes_cache[key] = data;
            return data
        }).catch(e => {
            let state = this.state;
            state.msg = e
            this.setState(state)
        })
    }

    regionChanged(region){
        if(!this.state.mounted){ return }

        let ne_lat = region.latitude - region.latitudeDelta;
        let ne_lng = region.longitude - region.longitudeDelta;
        let sw_lat = region.latitude + region.latitudeDelta;
        let sw_lng = region.longitude + region.longitudeDelta;
        let h = hash(ne_lat, ne_lng, sw_lat, sw_lng);
        let zoom = this.calculateZoom(region);

        if(h + zoom === this.current_hash){ return }
        this.current_hash = h + zoom;
        let delta = Math.min(region.longitudeDelta, region.latitudeDelta);

        this.getCachedRoutes(h, zoom).then(data => {
            let {routes, msg} = data;
            msg += `\ndelta:${delta}\nzoom:${zoom}`;

            this.setState({
                msg: msg,
                routes: routes,
                got_routes: true,
            });
        });
    }

    calculateZoom(region){
        let delta = Math.min(region.longitudeDelta, region.latitudeDelta);
        let bestZoom = null;
        [
            0.01,
            0.02,
            0.03,
            0.05,
            0.07,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            1,
            2,
            3,
        ].forEach((threshold, i) => {
            if(bestZoom === null && delta < threshold){
                bestZoom = 20-i;
            }
        });
        if(bestZoom === null){
            return 1
        }
        return bestZoom;
    }

    routes(){
        if(this.state.routes === undefined){ return []; }

        let routes = [];
        let existingKeys = [];
        this.state.routes.forEach(data => {
            if(data.lines === null){ return }
            if(data.lines === undefined){ return }

            let i = 0;
            let coordinates = [];
            data.lines.forEach(line => {
                let key = `${data.pubId}_${i}`;
                if(existingKeys.includes(key)){ return }
                line.forEach(coord => {
                   coordinates.push({latitude: coord[0], longitude: coord[1]})
                });
                let route = <Polyline key={key} coordinates={coordinates} />;
                existingKeys.push(key);
                routes.push(route);

            })
        });
        return routes;
    }

    render() {
        return (<>
            <MapView
                style={{ flex: 1, justifyContent: "center", alignItems: "center" }}
                showsUserLocation
                mapType="terrain"
                ref={map => {this.map = map}}
                onRegionChange={this.regionChanged.bind(this)}
            >
                {this.routes()}
            </MapView>

            <View style={{position:'absolute', backgroundColor: 'red', top: 150, width: "100%"}}>
                <Text>{this.state.msg}</Text>
            </View>
        </>);

    }
}


export default TriptracksApp;