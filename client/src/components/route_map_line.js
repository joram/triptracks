import React, {Component} from "react";
import {Polyline} from "react-google-maps";
import routeStore from "../routeStore";
import map_zoom_emitter from "../map_zoom_emitter";
import {withRouter} from "react-router-dom";


export class RouteMapLine extends Component {

    constructor(props) {
        super(props);
        this.pubId = this.props.pubId;
        this.state = {
            lines: {},  // key'ed on zoom
            current_zoom: this.props.zoom,
            bounds: [],
            showing_zoom: -1,
        };
        routeStore.subscribeGotRoutesWithPubId(this.moreDataForThisRoute.bind(this), this.pubId);
        map_zoom_emitter.subscribeZoomChange(this.zoomChanged.bind(this));
        this.addLines(this.props.hash, this.props.zoom);
    }

    componentDidMount() {
    this._ismounted = true;
    }

    componentWillUnmount() {
    this._ismounted = false;
    }

    zoomChanged(data) {
        let state = this.state;
        state.zoom = data.zoom;
        if(this._ismounted){
            this.setState(state);
        }
    }

    moreDataForThisRoute(data) {
        this.addLines(data.hash, data.zoom);
    }

    addLines(hash, zoom) {
        if (this.state.lines[zoom] !== undefined) {
            return
        }

        let polyLines = [];
        let route = routeStore.getRouteByHashZoomAndPubID(hash, zoom, this.pubId);
        if (route === undefined) {
            return
        }
        let state = this.state;
        state.bounds = route.bounds;
        if (route.lines === null) {
            if(this._ismounted){
                this.setState(state);
            }
            return
        }
        route.lines.forEach((line) => {
            if (line === null) {
                this.setState(state);
                return
            }

            let coordinates = [];
            line.forEach((coord) => {
                coordinates.push({lat: coord[0], lng: coord[1]});
            });

            polyLines.push(<Polyline
                key={"line_" + polyLines.length + 1 + "_" + this.state.pubId}
                path={coordinates}
                geodesic={true}
                onClick={this.clicked.bind(this)}
                options={{
                    strokeColor: "#ff2527",
                    strokeOpacity: 0.75,
                    strokeWeight: 2,
                }}
            />);
        });
        state.lines[zoom] = polyLines;
        if(this._ismounted){
            this.setState(state);
        }
    }

    clicked() {
        this.props.history.push(`/route/${this.pubId}`);
    }

    render() {
        let line = this.state.lines[this.state.current_zoom];
        if(line === undefined){
            return null
        }
        return line
    }
}


export default withRouter(RouteMapLine);
