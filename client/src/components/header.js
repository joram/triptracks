import React from "react";
import {Navbar, Nav, NavItem, NavDropdown, MenuItem, Image} from "react-bootstrap";
import { GoogleLogin } from 'react-google-login';

class MenuTitle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: this.props.name,
      imageUrl: this.props.imageUrl
    }
  }

  render() {
    return (
      <span>
        {this.state.name}
        <Image src={this.state.imageUrl} style={{width:35, marginLeft:5, padding:0, border:0}} thumbnail/>
      </span>
    )
  }
}

class Menu extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isLoggedIn: false
    }
  }


  loginSuccess(resp) {
    console.log("successful login ", resp)
    this.setState({
      isLoggedIn: true,
      googleData: resp,
    })
  }

  loginFailure(resp) {
    console.log("failed login ",resp)
    this.setState({isLoggedIn: false})
  }

  logoutSuccess(resp) {
    console.log("logout success ",resp)
    this.setState({isLoggedIn: false})
  }

  render() {
    if (this.state.isLoggedIn) {
      return (<Nav pullRight>
        <NavDropdown eventKey={3} title={<MenuTitle
            name={this.state.googleData.profileObj.name}
            imageUrl={this.state.googleData.profileObj.imageUrl}
          />} id="basic-nav-dropdown">
          <MenuItem eventKey={3.1}>Action</MenuItem>
          <MenuItem eventKey={3.2}>Another action</MenuItem>
          <MenuItem eventKey={3.3}>Something else here</MenuItem>
          <MenuItem divider/>
          <MenuItem eventKey={3.4}>Separated link</MenuItem>
        </NavDropdown>
      </Nav>)
    }
    return (<Nav pullRight><GoogleLogin
    clientId="965794564715-ebal2dv5tdac3iloedmnnb9ph0lptibp.apps.googleusercontent.com"
    buttonText="Login"
    onSuccess={this.loginSuccess.bind(this)}
    onFailure={this.loginFailure.bind(this)}
    onLogoutSuccess={this.logoutSuccess.bind(this)}
    /></Nav>)

  }


}

class Header extends React.Component {

  render(){
    return (
      <Navbar inverse style={{margin:0}}>
        <Navbar.Header>
          <Navbar.Brand style={{display: "flex", alignItems: "center"}} >
            <a href="#home">
              Triptracks
              <Image src="/favicon.ico" style={{width:35, marginTop: -7, float:"left", marginRight:5}} thumbnail/>
            </a>
          </Navbar.Brand>
        </Navbar.Header>
        <Menu />
      </Navbar>)
  }
}


export default Header;
