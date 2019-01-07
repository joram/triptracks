import React from "react";
import ReactDOM from "react-dom";
import MapContainer from "./components/map";

const Index = () => {
  return <div><MapContainer /></div>;
};

ReactDOM.render(<Index />, document.getElementById("index"));