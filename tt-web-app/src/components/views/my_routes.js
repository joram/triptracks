import React from "react";
import {CardGroup, Card, Image, Icon, Label, Segment} from "semantic-ui-react";
import { Link } from "react-router-dom";
import client from "../../api-client/client";
import {withGoogleMap, withScriptjs} from "react-google-maps";


class MyRoutes extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      favourite_routes: [],
      owner_routes: [],
    };
    client.subscribeGotUser(() => {
      this.updateStravaRoutes();
      this.updateBucketList();
    });
    if(client.isLoggedIn()){
      this.updateStravaRoutes();
      this.updateBucketList()
    }
  }

  updateStravaRoutes(){
    client.getStravaActivities().then(routes => {
      let state = this.state;
      state.owner_routes = routes;
      this.setState(state);
    })
  }

  updateBucketList(){
    client.getBucketListRoutes().then(routes => {
      let state = this.state;
      state.favourite_routes = routes;
      this.setState(state);
    })
  }

  removeFavourite(e, pubId){
    client.removeFromBucketList(pubId).then(() => {
      this.updateBucketList();
    });
    e.stopPropagation();
  }

  removeOwned(e, pubId){
    console.log("removing owned route", pubId);
    client.removeOwnedRoute(pubId).then(()=>{
      this.updateStravaRoutes();
    });
    e.stopPropagation();
  }

  _favourite_card(route){
      return <Card
        key={`my_routes_${route.pubId}`}
        onClick={() =>{this.props.onRouteSelect(route.pubId)}}
        as="div"
        style={{marginRight:"15px"}}
      >
          <Image fluid>
            <Link to={`/route/${route.pubId}`}>
              <img src={route.sourceImageUrl} alt=""/>
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
        <Card.Content>
          <Card.Header>{route.name}</Card.Header>
        </Card.Content>
      </Card>;
  }

  _owner_card(route){
      return <Card
        key={`my_routes_${route.pubId}`}
        onClick={() =>{this.props.onRouteSelect(route.pubId)}}
        as="div"
        style={{marginRight:"15px"}}
      >
          <Image fluid>
            <Link to={`/route/${route.pubId}`}>
              <img src={route.sourceImageUrl} alt=""/>
            </Link>
            <Label ribbon>
              <Icon name="user"/>
            </Label>
            <Label
              corner="right"
              circular
              onClick={(e) => {this.removeOwned(e, route.pubId)}}
            >
              <Icon name="remove circle" style={{top:"5px", right:"5px"}} />
            </Label>
          </Image>
        <Card.Content>
          <Card.Header>{route.name}</Card.Header>
        </Card.Content>
      </Card>;
  }

  cards(){
    let cards = [];
    this.state.favourite_routes.forEach(route => {
      cards.push(this._favourite_card(route))
    });
    this.state.owner_routes.forEach(route => {
      cards.push(this._owner_card(route))
    });
    return cards;
  }

  render() {
    return (<Segment basic style={{paddingTop:"15px", paddingLeft:"25px"}}>
          <CardGroup>{this.cards()}</CardGroup>
      </Segment>
    );
  }
}


export default withScriptjs(withGoogleMap(MyRoutes));