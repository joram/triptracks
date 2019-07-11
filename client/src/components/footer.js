import React from "react";
import {Segment} from "semantic-ui-react";


class Footer extends React.Component {

  render(){
    return (
      <Segment inverted basic style={{margin:0, padding:"8px"}} textAlign="center">
        <div style={{margin:"auto", color: "#aaaaaa", fontSize:"10px"}}>this is a footer, nobody bothers reading these. poop.</div>
      </Segment>
    )
  }
}


export default Footer;
