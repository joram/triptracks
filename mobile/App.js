import React, { Component } from 'react';
import MapView, { Polyline } from 'react-native-maps'
import * as Location from 'expo-location';
import { Text, View } from 'react-native';
import { hash, get_routes, get_routes_page } from './utils';


class TriptracksApp extends Component {

    constructor(props){
        super(props);
        this.map = null;
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
            this.forceUpdate()
        }

    }

    regionChanged(region){
        if(!this.state.mounted){ return }

        // todo: debounce
        if(!this.state.got_routes){

            let state = this.state;
            state.got_routes = true;
            this.setState(state);

            let ne_lat = region.latitude - region.latitudeDelta;
            let ne_lng = region.longitude - region.longitudeDelta;
            let sw_lat = region.latitude + region.latitudeDelta;
            let sw_lng = region.longitude + region.longitudeDelta;
            let h = hash(ne_lat, ne_lng, sw_lat, sw_lng);

            get_routes(h, 10).then(routes => {
                this.setState({
                    msg: `got new region\n${JSON.stringify(region)}\nhash = ${h}\ndata=${JSON.stringify(routes[0])}`,
                    routes: routes,
                    got_routes: true,
                });
            });
        }
    }

    routes(){
        let renderedRoutes = {};
        let routes = [];
        if(!this.state.got_routes){ return []; }
        if(this.state.routes === undefined){ return []; }

        this.state.routes.forEach(data => {
            if(data.lines === null){ return }
            if(data.lines === undefined){ return }
            if(renderedRoutes[data.pubId]){ return }
            data.lines.forEach(line => {
                let coordinates = [];
                line.forEach(coord => {
                   coordinates.push({latitude: coord[0], longitude: coord[1]})
                });

                let route = <Polyline key={data.pubId} coordinates={coordinates} />;
                routes.push(route);
                renderedRoutes[data.pubId] = true;
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