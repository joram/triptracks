import React from "react";
import Routes from "../routes";


class Home extends React.Component {
  render(){
    const styles = {
      width: window.innerWidth,
      height: window.innerHeight-54
    };

    return (<Routes
      googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
      loadingElement={<div style={styles} />}
      containerElement={<div style={styles} />}
      mapElement={<div style={styles} />}
    />)
  }
}

export default Home;