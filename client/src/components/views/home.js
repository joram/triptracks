import React from "react";
import log_graphql_errors from "../routes";
import Routes from "../routes";
import history from "../../history";
import {Container, Row, Col} from "react-bootstrap";

class RouteDetails extends React.Component {

  constructor(props) {
    super(props);
    let urlParams = new URLSearchParams(history.location.search);
    this.url = "https://app.triptracks.io/graphql";
    if (window.location.hostname === "localhost") {
      this.url = "http://127.0.0.1:8000/graphql";
    }
    this.state = {
      route: null,
      pubId: urlParams.get('route'),
    }

    if (this.state.pubId !== null) {
      this.getRoute(this.state.pubId).then(routeData => {
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
    if(this.state.pubId === null){
      return null;
    }
    if(this.state.route === null){
      return <div key="route_details" id="route_details" style={{
        float: "left",
        width:"300px",
        borderRight: "solid thin black",
        height: "50px",
        overflow: "hidden",
        textOverflow: "ellipsis",
      }} />
    }

    let style = {
      float: "left",
      width:"300px",
      borderRight: "solid thin black",
      height: "100%",
      overflow: "hidden",
      textOverflow: "ellipsis",
      maxHeight: "inherit",
      boxSizing: "border-box",
      padding: "5px",
    }

    return <div key="route_details" id="route_details" style={style}>
      <h3 style={{ width:"300px" }}>{this.state.route.name}</h3>

      {this.state.route.description}
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
      <div id="home">
        <Container fluid style={{padding: "0",
          width: "100%",
          height: "100%",
        }}>
          <Row style={{margin: 0}}>
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