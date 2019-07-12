import React from "react";
import history from "../history";
import routeStore from '../routeStore'


class RouteDetails extends React.Component {

    constructor(props) {
        super(props);
        this.state = {route: null};
        routeStore.subscribeGotRouteByPubId(this.gotRoute.bind(this));

        history.listen((a, b) => {
            let pub_id = this.url_pub_id();
            if (pub_id !== undefined) {
                routeStore.getRouteByID(pub_id);
            }
        });

        let pub_id = this.url_pub_id();
        if (pub_id !== undefined) {
            routeStore.getRouteByID(pub_id);
        }

    }

    url_pub_id() {
        let urlParams = new URLSearchParams(history.location.search);
        return urlParams.get('route');
    }

    gotRoute() {
        let route = routeStore.getRouteByID2(this.url_pub_id());
        this.setState({route: route})
    }

    render() {
        let style = {
            left: "0",
            width: "300px",
            border: "solid thin black",
            height: `${window.innerHeight}px`,
            overflow: "hidden",
            backgroundColor: "lightblue",
            textOverflow: "ellipsis",
            position: "absolute",
        };

        if (this.state.route === null) {
            return null
        }

        return <div key="route_details" id="route_details" style={style}>
            <h3 style={{
                width: "300px",
                fontSize: "20px",
                marginBottom: "0px",
                paddingTop: "5px",
                textAlign: "center"
            }}>{this.state.route.name}</h3>
            <img src={this.state.route.sourceImageUrl} style={{width: "100%", padding: "5px"}}/>
            {this.state.route.description}
        </div>
    }
}

export default RouteDetails;