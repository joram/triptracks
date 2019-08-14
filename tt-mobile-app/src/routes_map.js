import React, { Component } from 'react';
import MapView, { Polyline } from 'react-native-maps'
import * as Location from 'expo-location';
import {hash, get_routes} from "./api-client/utils"

class Route extends Component {

    constructor(props){
        super(props);
        this.lines = {};
        this.pubId = this.props.pubId;
        this.getZoom = this.props.getZoom;
        this.buildPolyLines(this.props.data)
    }

    buildPolyLines(data){
        let polylines = [];
        if(data.lines === null){ return }
        if(data.lines === undefined){ return }

        let i = 0;
        data.lines.forEach(line => {
            let coordinates = [];
            line.forEach(coord => {
               coordinates.push({latitude: coord[0], longitude: coord[1]})
            });

            polylines.push(<Polyline key={data.pubId} coordinates={coordinates} />);
        });

        this.lines[`${data.pubId}_${data.zoom}`] = polylines;
    }

    getPolylines(){
        let r = this.lines[`${this.pubId}_${this.getZoom()}`];
        if(r !== undefined) return r
        return Object.values(this.lines)[0]
    }

    render(){
        console.log("rendering ", this.pubId);
        return this.getPolylines()
    }
}


class RoutesMap extends Component {

    constructor(props){
        super(props);
        this.map = null;
        this.routes = {};
        this.region = null;
        this.lock = false;
        this.state = {};

        // monitor location
        let options = { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 };
        Location.requestPermissionsAsync();
        Location.hasServicesEnabledAsync().then(enabled => {
            if(enabled){
                Location.watchPositionAsync(options, this.positionUpdated.bind(this));
                Location.getCurrentPositionAsync(options).then(position => {
                    this.positionUpdated(position, true);
                });
                return
            }

            Location.requestPermissionsAsync().then(() => {
                Location.watchPositionAsync(options, this.positionUpdated.bind(this))
            })
        });
    }

    getZoom(){
        return this.calculateZoom(this.region)
    }

    positionUpdated(position, snapTo=false){
        const { latitude, longitude } = position.coords;
        let region = {
            latitude: latitude,
            longitude: longitude,
            latitudeDelta: 0.08,
            longitudeDelta: 0.08,
        };
        this.region = region;
        if(snapTo){
            this.map.animateToRegion(region);
        }
        return this.updateRoutes(region);
    }


    async updateRoutes(region){
        if(this.map === null){
            console.log("no map, no update");
            return
        }
        if(this.lock){
            return
        }
        this.lock = true;
        console.log("updating routes");

        this.map.animateToRegion(region);
        let ne_lat = region.latitude - region.latitudeDelta;
        let ne_lng = region.longitude - region.longitudeDelta;
        let sw_lat = region.latitude + region.latitudeDelta;
        let sw_lng = region.longitude + region.longitudeDelta;
        let h = hash(ne_lat, ne_lng, sw_lat, sw_lng);
        let zoom = this.calculateZoom(region);
        return await get_routes(h, zoom).then(routes => {
            console.log(`got ${routes.length} routes`);
            routes.forEach(route => {
                if(this.routes[route.pubId] !== undefined){
                    // this.routes[route.pubId].buildPolyLines(route);
                } else {
                   this.routes[route.pubId] = <Route data={route} getZoom={this.getZoom.bind(this)}/>;
                }
            });
            this.forceUpdate();
            this.lock = false;
        })
    }

    getRoutes(){
        console.log(Object.keys(this.routes));
        return Object.values(this.routes);
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

    render() {
        console.log(`rendering map with ${this.getRoutes().length} routes`)
        return (<>
            <MapView
                style={{ flex: 1, justifyContent: "center", alignItems: "center" }}
                showsUserLocation
                mapType="terrain"
                ref={map => {this.map = map}}
                onRegionChange={this.updateRoutes.bind(this)}
            >
                {this.getRoutes()}
            </MapView>
        </>);

    }
}


export default RoutesMap