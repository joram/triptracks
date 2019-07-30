import React from "react";
import RoutesMap from "../routes_map";
import RouteSidePanel from "../route_side_panel"
import {Sidebar, Segment} from "semantic-ui-react";


class Home extends React.Component {

  constructor(props) {
    super(props);
    let pub_id = null;
    if(this.props.route !== null){
      pub_id = this.props.route.pub_id;
    }
    this.state = {
      routePubId: pub_id
    }
    window.addEventListener('resize', this.onResize.bind(this));
  }

  onResize(){
    this.forceUpdate()
  }

  render(){
    const styles = {
      height: `${window.innerHeight - 92}px`,
    };

    let route_map = <RoutesMap
      googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
      loadingElement={<div id="map_loading_element" style={styles} />}
      containerElement={<div id="map_container" />}
      mapElement={<div id="map_element" style={styles} />}
      key="routes"
      route={this.props.route}
      onRouteSelect={this.props.onRouteSelect}
    />;

    return (<Sidebar.Pushable as={Segment} style={{marginTop:0, marginBottom:0}}>
      <Sidebar as={Segment} animation="overlay" direction="left" visible={this.props.route !== null} style={{height:"500px"}}>
        <RouteSidePanel route={this.props.route}/>
      </Sidebar>
      <Sidebar.Pusher style={{marginLeft: "0 !important", marginRight: "0 !important", width: "auto"}}>
        {route_map}
      </Sidebar.Pusher>
    </Sidebar.Pushable>)
  }
}

export default Home;