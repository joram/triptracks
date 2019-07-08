import React, { Component } from 'react';
 import { PermissionsAndroid } from 'react-native';
import MapView, { Polyline } from 'react-native-maps'


async function requestCameraPermission() {
  try {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_COARSE_LOCATION,
      {
        title: 'Cool Photo App Camera Permission',
        message:
          'Cool Photo App needs access to your camera ' +
          'so you can take awesome pictures.',
        buttonNeutral: 'Ask Me Later',
        buttonNegative: 'Cancel',
        buttonPositive: 'OK',
      },
    );
    if (granted === PermissionsAndroid.RESULTS.GRANTED) {
      console.log('You can use the camera');
    } else {
      console.log('Camera permission denied');
    }
  } catch (err) {
    console.warn(err);
  }
}

class TriptracksApp extends Component {

  positionUpdated(newPosition){
        const { latitude, longitude } = newPosition.coords;
        console.log(latitude, longitude);

  }

  componentDidMount() {
    requestCameraPermission().catch(error =>{
      console.log(error)
    });
    let options = { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 };
    this.watchID = navigator.geolocation.watchPosition(
      this.positionUpdated.bind(this),
      error => console.log(error),
      options,
    );
  }

  lines(){
    return [<Polyline
		coordinates={[
			{ latitude: 37.8025259, longitude: -122.4351431 },
			{ latitude: 37.7896386, longitude: -122.421646 },
			{ latitude: 37.7665248, longitude: -122.4161628 },
			{ latitude: 37.7734153, longitude: -122.4577787 },
			{ latitude: 37.7948605, longitude: -122.4596065 },
			{ latitude: 37.8025259, longitude: -122.4351431 }
		]}
		strokeColor="#000" // fallback for when `strokeColors` is not supported by the map-provider
		strokeColors={[
			'#7F0000',
			'#00000000', // no color, creates a "long" gradient between the previous and next coordinate
			'#B24112',
			'#E5845C',
			'#238C23',
			'#7F0000'
		]}
		strokeWidth={6}
	/>]
  }

  render() {
    return (
      <MapView style={{ flex: 1}}>
        {this.lines()}
      </MapView>
    );
  }
}


export default TriptracksApp;