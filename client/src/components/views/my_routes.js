import React from "react";
import {Segment, CardGroup, Card, Image} from "semantic-ui-react";
import { Link } from "react-router-dom";
import routeStore from "../../routeStore";


class MyRoutes extends React.Component {

  my_route_ids = [
    "route_ca8f3800be1cafe3bc654665de2bffe4",
    "route_18be4c4655534e879399aff2b092d56c",
    "route_984f8aed7d480494582b14559bd4d929",
    "route_babc58aa227295a7c932681a36aa6b8d",
  ];

  constructor(props){
    super(props);
    this.state = {route_cards:[]};
    this.updateRouteCards(this.my_route_ids);
  }

  updateRouteCards(routes){
    let cards = [];
    routes.forEach(pub_id => {
      routeStore.getRouteByID(pub_id).then( route => {
        let card = <Card
          as={Link}
          key={`my_routes_${route.pubId}`}
          to={`/route/${route.pubId}`}
          onClick={() =>{this.props.onRouteSelect(route.pubId)}}
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
      })
    });

  }

  render() {
    return (<Segment>
          <CardGroup>{this.state.route_cards}</CardGroup>
      </Segment>
    );
  }
}


export default MyRoutes;