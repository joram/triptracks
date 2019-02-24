import React from "react";
import Routes from "../routes";



class Home extends React.Component {

  render(){
    const styles = {
      width: "100%",
      height: `${window.innerHeight-100}px`
    };

    return <Routes
      key="routes"
    />
  }
}

export default Home;