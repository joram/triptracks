import React from "react";
import {Container, CardGroup, Card, Image, Icon} from "semantic-ui-react";
import { Link } from "react-router-dom";
import client from "../../api-client/client";
import {withGoogleMap, withScriptjs} from "react-google-maps";


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
    })
  }

  removeFavourite(e, pubId){
    client.removeFromBucketList(pubId).then(() => {
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
        key={`my_routes_${route.pubId}`}
        onClick={() =>{this.props.onRouteSelect(route.pubId)}}
        as="div"
      >
        <Icon
          size="large"
          name="heart"
          style={{position:"absolute", float:"right", right:0, zIndex:999}}
          onClick={(e) =>{this.removeFavourite(e, route.pubId)}}
        />
        <Link to={`/route/${route.pubId}`} >
          <Image src={route.sourceImageUrl} wrapped />
        </Link>
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


export default withScriptjs(withGoogleMap(MyRoutes));