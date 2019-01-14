import React from "react";
import ReactDOM from "react-dom";
import Favicon from 'react-favicon';
import Header from "./components/header";
import Map from "./components/map";
require('../assets/images/favicon.ico');

class Index extends React.Component {
  render() {
    const styles = {
      width: window.innerWidth,
      height: window.innerHeight-54
    }
    return (<div>
      <Favicon url="/favicon.ico"/>
      <Header/>
      <Map
        googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
        loadingElement={<div style={styles} />}
        containerElement={<div style={styles} />}
        mapElement={<div style={styles} />}
      />
    </div>)
  }
}

ReactDOM.render(<Index />, document.getElementById("index"));