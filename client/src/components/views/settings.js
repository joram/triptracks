import React from "react";
import connect_strava_icon from '../../connect_strava.svg';
import {Segment, Image, Button} from "semantic-ui-react";


class Settings extends React.Component {
  connectStrava(){
    console.log("connecting strava")
  }

    //  style={{height:48, width:193, border:"solid thin gray"}} rounded
  render() {
    return (<Segment>
      <Button onClick={this.connectStrava}>
        <Image src={connect_strava_icon} />
      </Button>
    </Segment>);
  }
}


export default Settings;