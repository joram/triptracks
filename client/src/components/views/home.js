import React from "react";
import RoutesMap from "../routes_map";
import RouteSidePanel from "../route_side_panel"
import {Container, Grid} from "semantic-ui-react";


class Home extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      showing_route_details: props.pub_id
    }
    window.addEventListener('resize', this.onResize.bind(this))
    console.log(`constructor for home: ${props.pub_id}`)
  }

  onResize(){
    this.forceUpdate()
  }

  render(){
    const styles = {
      width: "100%",
      height: `${window.innerHeight - 92}px`,
    };
    let container_style = {
      width: "100%",
      marginLeft: "0px",
    };

    let route_map = <RoutesMap
      googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
      loadingElement={<div id="map_loading_element" style={styles} />}
      containerElement={<div id="map_container" style={container_style} />}
      mapElement={<div id="map_element" style={styles} />}
      key="routes"
      centerOnPubId={this.props.pub_id}
    />;

    if(this.props.pub_id === undefined){
      return route_map
    }

    return (<Container style={{margin:0}}>
      <Grid>
        <Grid.Row>
          <Grid.Column width={4} style={{padding:0}}>
            <RouteSidePanel pub_id={this.props.pub_id} />
          </Grid.Column>
            <Grid.Column width={12} style={{padding:0}}>
              {route_map}
            </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>)
  }
}

export default Home;