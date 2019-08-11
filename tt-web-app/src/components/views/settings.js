import React from "react";
import connect_strava_icon from '../../connect_strava.svg';
import {Segment, Image, Button, Grid} from "semantic-ui-react";
import {get_params} from "../../utils";
import client from "../../api-client/client";

let redirect_uri = window.location.href;
let strava_auth_url = `http://www.strava.com/oauth/authorize` +
  `?client_id=29431` +
  `&response_type=code` +
  `&redirect_uri=${redirect_uri}` +
  `&approval_prompt=force&scope=activity:read_all`;


class Settings extends React.Component {

  constructor(props){
    super(props);
    let code = get_params(this.props)["code"];
    if(code !== undefined){
      client.subscribeGotUser(() => {
        console.log("connecting to strava")
        client.connectToStrava(code).then(data =>{console.log(data)})
      })
    }
  }

  render() {
    return (<Segment basic>
        <Grid columns={2}>
      <Grid.Row>
        <Grid.Column>
          <a href={strava_auth_url}>
            <Image src={connect_strava_icon}  style={{border: "solid thin black"}}/>
          </a>
        </Grid.Column>
        <Grid.Column>
          We create private routes from each of your strava activities, so you can easily share new trails with us on triptracks.
          Once you have created a new strava activity, you can see it under <a href="/routes">My Routes</a>
        </Grid.Column>
      </Grid.Row>
    </Grid>
    </Segment>);
  }
}


export default Settings;