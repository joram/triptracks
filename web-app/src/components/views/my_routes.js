import React from "react";
import {Container, CardGroup, Card, Image} from "semantic-ui-react";
import { Link } from "react-router-dom";
import client from "../../api-client/client";


class MyRoutes extends React.Component {

  constructor(props){
    super(props);
    this.state = {route_cards:[]};
    client.subscribeGotUser(this.updateBucketList.bind(this))
    if(client.isLoggedIn()){
      this.updateBucketList()
    }
  }

  updateBucketList(){
    client.getBucketListRoutes().then(routes => {
      console.log("my routes:", routes);
      this.updateRouteCards(routes);
    })
  }

  updateRouteCards(routes){
    let cards = [];
    console.log(routes);
    routes.forEach(route => {
      console.log(route);
      let card = <Card
        as={Link}
        key={`my_routes_${route.pubId}`}
        to={`/route/${route.pubId}`}
        onClick={() =>{this.props.onRouteSelect(route.pubId)}}
         size="mini"
        color="olive"
      >
        <Image src={route.sourceImageUrl} wrapped ui={false} />
        <Card.Content>
          <Card.Header>{route.name}</Card.Header>
        </Card.Content>
      </Card>;

      cards.push(card);
      let state = this.state;
      state.route_cards = cards;
      this.setState(state);
    });

  }

  render() {
    return (<Container style={{paddingTop:"15px"}}>
          <CardGroup>{this.state.route_cards}</CardGroup>
      </Container>
    );
  }
}


export default MyRoutes;