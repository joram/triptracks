import React from "react";
import {Navbar, Nav, NavDropdown, MenuItem, Image} from "react-bootstrap";
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import RoutesSearch from './routeSearch'


const PROFILE_MENU_ACTIONS = {
  ROUTES: 0,
  PLANS: 1,
  SETTINGS: 2,
  LOGOUT: 3,
};

class ProfileMenuTitle extends React.Component {

  render() {
    return (
      <span>
        {this.props.name}
        <Image src={this.props.imageUrl} style={{width:35, marginLeft:5, padding:0, border:0}} thumbnail/>
      </span>
    )
  }
}

class ProfileMenu extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isLoggedIn: false
    }
  }

  loginSuccess(resp) {
    this.setState({
      isLoggedIn: true,
      googleData: resp,
    })
  }

  loginFailure(resp) {
    console.log("failed login ",resp);
    this.setState({isLoggedIn: false})
  }

  logoutSuccess(resp) {
    console.log("logout success ",resp);
    this.setState({isLoggedIn: false})
  }

  render() {
    let content = <GoogleLogin
      clientId="965794564715-ebal2dv5tdac3iloedmnnb9ph0lptibp.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={this.loginSuccess.bind(this)}
      onFailure={this.loginFailure.bind(this)}
      onLogoutSuccess={this.logoutSuccess.bind(this)}
      isSignedIn={true}
    />;
    if (this.state.isLoggedIn) {
      let title = <ProfileMenuTitle
        name={this.state.googleData.profileObj.name}
        imageUrl={this.state.googleData.profileObj.imageUrl}
      />;
      content = <NavDropdown eventkey={3} title={title} id="basic-nav-dropdown">
        <NavDropdown.Item eventKey={PROFILE_MENU_ACTIONS.ROUTES}>My Routes</NavDropdown.Item>
        <NavDropdown.Item eventKey={PROFILE_MENU_ACTIONS.PLANS}>My Plans</NavDropdown.Item>
        <NavDropdown.Item eventKey={PROFILE_MENU_ACTIONS.SETTINGS}>Settings</NavDropdown.Item>
        <NavDropdown.Item eventKey={PROFILE_MENU_ACTIONS.LOGOUT}>
          <GoogleLogout
            buttonText="Logout"
            onLogoutSuccess={this.logoutSuccess.bind(this)}
            render={renderProps => (<div onClick={renderProps.onClick}>Logout</div>)}
          />
        </NavDropdown.Item>
      </NavDropdown>;
    }

    return <Nav className="justify-content-end" >{content}</Nav>
  }


}

class Header extends React.Component {

  menuSelect(eventKey) {
    if(eventKey === PROFILE_MENU_ACTIONS.LOGOUT){
      return
    }
    this.props.root.changeView(eventKey);
  }

  render(){
    return (
      <Navbar onSelect={this.menuSelect.bind(this)} bg="dark" variant="dark">
        <Navbar.Brand>
          <a href="#home" style={{color: "#AAAAAA", fontSize:"28px"}}>
            Triptracks
            <Image src="/favicon.ico" style={{width:35, float:"left", marginRight:5}} thumbnail/>
          </a>
        </Navbar.Brand>
        <RoutesSearch/>
        <ProfileMenu/>
      </Navbar>
    )
  }
}


export default Header;
