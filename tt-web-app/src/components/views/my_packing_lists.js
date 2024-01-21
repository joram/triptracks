import React from "react";
import {Segment, List, Icon, Button} from "semantic-ui-react";
import { Link } from "react-router-dom";
import client from "../../api-client/client";
import {log_graphql_errors} from "../../api-client/utils";

const dateformat = require('dateformat');


class MyPackingLists extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      plans: [],
    };
    client.subscribeGotUser(() => {
      this.getTripPlans();
    });
    if(client.isLoggedIn()){
      this.getTripPlans();
    }
  }

  getTripPlans(){
    client.getTripPlans().then(plans => {
      log_graphql_errors("getting trips", plans);
      let state = this.state;
      state.plans = plans;
      this.setState(state);
    });
  }

  deletePlan(e, pub_id){
    e.preventDefault();
    client.deleteTripPlan(pub_id).then(data => {
      this.getTripPlans();
    })
  }

  cards(){
    let cards = [];
    cards.push(
      <List.Item key="new" to="/packing_list/create" as={Link}>
        <List.Content align="center">
          <List.Header>
            <List.Icon name="plus" size='large' verticalAlign='middle' floated="left"/>
            New Packing List
          </List.Header>
        </List.Content>
      </List.Item>
    );
    this.state.plans.forEach(plan => {
      let datetime_str = "not scheduled";
      if(plan.startDatetime !== null && plan.endDatetime !== null){
        let s = new Date(plan.startDatetime);
        let e = new Date(plan.endDatetime);
        let diffDays = parseInt((e-s)/(24*3600*1000));
        datetime_str = `${dateformat(plan.startDatetime, "mmmm dS, yyyy")} (${diffDays} days)`
      }

      cards.push(
      <List.Item key={plan.pubId} to={"/plan/"+plan.pubId} as={Link}>
        <List.Content floated="left">
          <List.Header>
            <List.Icon name="road" size='large' verticalAlign='middle' floated="left"/>
            {plan.name}
          </List.Header>
          <List.Description>{plan.summary}</List.Description>
        </List.Content>
        <List.Content floated="right">
          {datetime_str}
          <Button icon onClick={(e) => {this.deletePlan(e, plan.pubId)}} color="red" style={{marginLeft:"10px"}}>
            <Icon name='delete' />
          </Button>
        </List.Content>
      </List.Item>

      );
    });
    return cards;
  }

  render() {
    return (<Segment basic>
      <List divided relaxed>
        {this.cards()}
      </List>
    </Segment>);
  }
}


export default MyPackingLists;