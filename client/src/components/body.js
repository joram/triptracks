import React from "react";
import Home from "./views/home";
import Settings from "./views/settings"

class Body extends React.Component {

  render(){
    if(this.props.view === "home")
      return (<Home />);

    if(this.props.view === "settings")
      return (<Settings/>);
  }
}


export default Body;