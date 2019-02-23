import React from "react";
import {Navbar} from "react-bootstrap";


class Footer extends React.Component {

  render(){
    return (
      <Navbar fixed="bottom" bg="dark" variant="dark">
        <div style={{margin:"auto", color: "#aaaaaa"}}>this is a footer, nobody bothers reading these. poop.</div>
      </Navbar>
    )
  }
}


export default Footer;
