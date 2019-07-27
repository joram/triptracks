import React from "react";
import {Container, CardGroup, Card, Image, Icon, Label, Segment} from "semantic-ui-react";
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
    routes.forEach(route => {

      let card = <Card
        key={`my_routes_${route.pubId}`}
        onClick={() =>{this.props.onRouteSelect(route.pubId)}}
        as="div"
        style={{marginRight:"15px"}}
      >
        <Container fluid style={{margin: "0!important"}} >
          <Image fluid>
            <Link to={`/route/${route.pubId}`}>
              <img src={route.sourceImageUrl}  />
            </Link>
            <Label ribbon>
              <Icon name="heart"/>
            </Label>
            <Label
              corner="right"
              circular
              onClick={(e) => {this.removeFavourite(e, route.pubId)}}
            >
              <Icon name="remove circle" style={{top:"5px", right:"5px"}} />
            </Label>
          </Image>
        </Container>
        <Card.Content>
          <Card.Header>{route.name}</Card.Header>
        </Card.Content>
      </Card>;

      cards.push(card);
      let state = this.state;
      state.route_cards = cards;
      state.num_cards = cards.length;
      this.setState(state);
    });

  }

  render() {
    return (<Container style={{paddingTop:"15px", marginBottom:"20px"}}>
          <CardGroup>{this.state.route_cards}</CardGroup>
      </Container>
    );
  }
}


export default withScriptjs(withGoogleMap(MyRoutes));