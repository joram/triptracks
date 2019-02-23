import React from "react";
import log_graphql_errors from "../routes";
import Routes from "../routes";
import history from "../../history";
import {Container, Row, Col} from "react-bootstrap";

class RouteDetails extends React.Component {

  constructor(props) {
    super(props);
    this.url = "https://app.triptracks.io/graphql";
    if (window.location.hostname === "localhost") {
      this.url = "http://127.0.0.1:8000/graphql";
    }
    this.state = {
      route: null
    }

    let urlParams = new URLSearchParams(history.location.search);
    let showingPubId = urlParams.get('route');
    if (showingPubId !== null) {
      this.getRoute(showingPubId).then(routeData => {
        console.log("showing route " + showingPubId + routeData);
        console.log(routeData);
        this.state.route = routeData;
        this.forceUpdate()
      });
    }
  }

  async getRoute(pubId){

    let query = `
      query get_single_route {
        route(pubId:"${pubId}"){
          pubId
          name
          description
          owner{
            pubId
          }
        }
      }
    `;

    let body = JSON.stringify({query});
    return await fetch(this.url, {
      method: 'POST',
      mode: "cors",
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: body
    })
    .then(r => r.json())
    .then(data => {
      return data.data.route;
    });
  }

  render() {
    let style = {
      float: "left",
      width:"300px",
      borderRight: "solid thin black",
      height: "100%",
      overflow: "hidden",
      textOverflow: "ellipsis",
    }
    if(this.state.route === null){
      return <div key="route_details" id="route_details" style={{
      float: "left",
      width:"300px",
      borderRight: "solid thin black",
      height: "50px",
      overflow: "hidden",
      textOverflow: "ellipsis",
    }}></div>
    }
    return <div key="route_details" id="route_details" style={{
      float: "left",
      width:"300px",
      borderRight: "solid thin black",
      height: "100%",
      overflow: "hidden",
      textOverflow: "ellipsis",
    }}>
      <div style={{
        float: "left",
        width:"300px",
        borderRight: "solid thin black",
        height: "100%",
        overflow: "hidden",
        textOverflow: "ellipsis",
        position: "absolute",
      }} >
        <h1>{this.state.route.name}</h1>
        <div  style={style}>
          <p  style={style}>{this.state.route.description}</p>
        </div>
      </div>
    </div>

  }
}

class Home extends React.Component {

  render(){
    const styles = {
      width: "100%",
      height: `${window.innerHeight-54}px`
    };

    return (
      <div>
        <RouteDetails />
        <Container fluid style={{padding: 0}}>
          <Row>
            <Col xs={12} style={{padding: 0}}>
              <Routes
                key="routes"
                googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
                loadingElement={<div id="map_loading_element" style={styles} />}
                containerElement={<div id="map_container" style={styles} />}
                mapElement={<div id="map_element" style={styles} />}
              />
            </Col>
          </Row>
        </Container>
      </div>
    )
  }
}

export default Home;