import React, { Component } from "react";
import Polyline, {Map} from "google-maps-react";

export class RouteContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showingInfoWindow: false,
      activeMarker: {},
      selectedPlace: {}
    };
  }

  render() {
    const pathCoordinates = [
      {lat: 36.05298765935, lng: -112.083756616339},
      {lat: 36.2169884797185, lng: -112.056727493181}
    ];
    return (<Polyline
        google={this.props.google}
        path={pathCoordinates}
        geodesic={true}
        options={{
            strokeColor: "#ff2527",
            strokeOpacity: 0.75,
            strokeWeight: 2,
            icons: [],
        }}
    />)
  }
}


export default RouteContainer;
