import React, { Component } from 'react';
import MapView from 'react-native-maps'
import * as Location from 'expo-location';
import { Text, View } from 'react-native';


class TriptracksApp extends Component {

  constructor(props){
      super(props);
      this.map = null;
      this.state = {
          msg: "Hello World",
      }
  }

  componentDidMount() {
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
    })
  }

  positionUpdated(position){
    const { latitude, longitude } = position.coords;
      let region  ={
        latitude: latitude,
        longitude: longitude,
        latitudeDelta: 0.004,
        longitudeDelta: 0.004,
        };
      this.setState({
          msg: `got new location, ${JSON.stringify(region)}`,
          position: position
      });

      if(this.map !== null){
        this.map.animateCamera({latitude, longitude});
        this.map.animateToRegion(region);
      }
  }

  render() {
      return (
      <MapView
          style={{ flex: 1, justifyContent: "center", alignItems: "center" }}
          showsUserLocation
          ref={map => {this.map = map}}
      >
      </MapView>
    );

    return <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <Text>
            {JSON.stringify(this.state.msg)}
        </Text>
    </View>
  }
}


export default TriptracksApp;