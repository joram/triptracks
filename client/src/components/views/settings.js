import React from "react";
import {Grid, Row, Tabs, Tab, Image} from "react-bootstrap";
require('../../../../client_old/assets/images/connect_strava.svg');


class Settings extends React.Component {
  connectStrava(){
    console.log("connecting strava")
  }

  render() {
    return (
      <Grid>
        <Row className="show-grid">
          <Tabs id="settings">
            <Tab eventKey={1} title="integrations">
              Strava
              <br/>
              <Image src="connect_strava.svg" onClick={this.connectStrava}  style={{height:48, width:193, border:"solid thin gray"}} rounded/>
            </Tab>
          </Tabs>
        </Row>
      </Grid>
    );
  }
}


export default Settings;