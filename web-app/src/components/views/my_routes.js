import React from "react";
import {Container, CardGroup, Card, Image, Icon} from "semantic-ui-react";
import { Link } from "react-router-dom";
import client from "../../api-client/client";


class MyRoutes extends React.Component {

  constructor(props){
    super(props);
    this.state = {route_cards:[]};
    client.subscribeGotUser(this.updateBucketList.bind(this));
    if(client.isLoggedIn()){
      this.updateBucketList()
    }
  }

  updateBucketList(){
    client.getBucketListRoutes().then(routes => {
      this.updateRouteCards(routes);
      console.log("updated bucket list")
    })
  }

  removeFavourite(e, pubId){
    console.log(e)
    client.removeFromBucketList(pubId).then(() => {
      console.log("removed a favourite");
      this.updateBucketList();
    });
    e.stopPropagation();
  }

  updateRouteCards(routes){
    let cards = [];
    console.log(routes);
    routes.forEach(route => {
      console.log(route);
      let card = <Card
        // as={Link}
        key={`my_routes_${route.pubId}`}
        // to={`/route/${route.pubId}`}
        onClick={() =>{this.props.onRouteSelect(route.pubId)}}
      >
        <Icon
          circular
          size={"large"}
          name="heart"
          style={{position:"absolute", float:"right", right:0, zIndex:1}}
          onClick={(e) =>{this.removeFavourite(e, route.pubId)}}
        />
        <Image src={route.sourceImageUrl} wrapped/>
        <Card.Content>
          <Card.Header>{route.name}</Card.Header>
        </Card.Content>
      </Card>;

      cards.push(card);
      let state = this.state;
      state.route_cards = cards;
      state.num_cards = cards.length;
      console.log(state)
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