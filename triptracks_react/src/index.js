import React from "react";
import ReactDOM from "react-dom";
import MapContainer from "./components/map";
import Favicon from 'react-favicon';
import RouteContainer from "./components/route";
require('../assets/images/favicon.ico');

const Index = () => {
  return <div>
    <Favicon url="/favicon.ico"/>
    <MapContainer/>
  </div>;
};

ReactDOM.render(<Index />, document.getElementById("index"));