"use strict";

import React from "react";
import ReactDOM from "react-dom";
import Favicon from 'react-favicon';
import Header from "./components/header";
import Body from "./components/body"
import {Container, Row, Col} from "react-bootstrap";

require('../assets/images/favicon.ico');
require("babel-core/register");
require("babel-polyfill");

class Index extends React.Component {


  constructor(props) {
    super(props);
    this.state = {
      view: "home",
    };
  }

  changeView(view){
    if(view === 2){
      this.setState({view: "settings"})
    }
  }

  render() {
    return (<div>
      <Favicon url="/favicon.ico"/>
      <Header root={this} />
      <Body view={this.state.view} history={history} />
    </div>)
  }
}

ReactDOM.render(<Index />, document.getElementById("index"));