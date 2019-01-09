import React, { Component } from "react";
import { Map, GoogleApiWrapper } from "google-maps-react";
import RouteContainer from "./route.js"

export class MapContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showingInfoWindow: false,
      activeMarker: {},
      selectedPlace: {}
    };
  }
  render() {
    if (!this.props.google) {
      return <div>Loading...</div>;
    }

    return (
      <div
        style={{
          position: "relative",
          height: "calc(100vh - 20px)"
        }}
      >
        <Map style={{}} google={this.props.google} zoom={14}>
        </Map>
          <RouteContainer/>
      </div>
    );
  }
}
export default GoogleApiWrapper({
  apiKey: "AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g",
  v: "3.30"
})(MapContainer);
