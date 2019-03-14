import React from "react";
import Routes from "../routes";
import history from "../../history";

class Home extends React.Component {

  constructor(props) {
    super(props);
    this.state = {showing_route_details: this.pub_id_in_url()}
    history.listen((a, b) => {
      this.setState({showing_route_details: this.pub_id_in_url()})
    });
  }

  pub_id_in_url(){
    let urlParams = new URLSearchParams(history.location.search);
    let pubId = urlParams.get('route');
    return pubId !== null;
  }


  render(){
    const styles = {
      width: "100%",
      height: `${window.innerHeight-95}px`
    };
    let container_style = {
      width: "100%",
      marginLeft: "0px",
    };

    if(this.state.showing_route_details){
      container_style.marginLeft = "300px";
      container_style.width = `${window.innerWidth-300}px`;
      container_style.height = `${window.innerHeight}px`
    }

    return <Routes
      googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
      loadingElement={<div id="map_loading_element" style={styles} />}
      containerElement={<div id="map_container" style={container_style} />}
      mapElement={<div id="map_element" style={styles} />}
      key="routes" />
  }
}

export default Home;