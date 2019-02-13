import React from "react";
import {Navbar, Nav, NavDropdown, MenuItem, Image} from "react-bootstrap";
import { GoogleLogin, GoogleLogout } from 'react-google-login';

const PROFILE_MENU_ACTIONS = {
  ROUTES: 0,
  PLANS: 1,
  SETTINGS: 2,
  LOGOUT: 3,
};

class ProfileMenuTitle extends React.Component {
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
    if (this.state.isLoggedIn) {
      return (<Nav pullRight>
        <NavDropdown eventKey={3} title={<ProfileMenuTitle
            name={this.state.googleData.profileObj.name}
            imageUrl={this.state.googleData.profileObj.imageUrl}
          />} id="basic-nav-dropdown"
        >
          <MenuItem eventKey={PROFILE_MENU_ACTIONS.ROUTES}>My Routes</MenuItem>
          <MenuItem eventKey={PROFILE_MENU_ACTIONS.PLANS}>My Plans</MenuItem>
          <MenuItem eventKey={PROFILE_MENU_ACTIONS.SETTINGS}>Settings</MenuItem>
          <MenuItem eventKey={PROFILE_MENU_ACTIONS.LOGOUT}>
            <GoogleLogout
              buttonText="Logout"
              onLogoutSuccess={this.logoutSuccess.bind(this)}
              render={renderProps => (<div onClick={renderProps.onClick}>Logout</div>)}
            ></GoogleLogout>
          </MenuItem>
        </NavDropdown>
      </Nav>)
    }
    return (<Nav pullRight><GoogleLogin
      clientId="965794564715-ebal2dv5tdac3iloedmnnb9ph0lptibp.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={this.loginSuccess.bind(this)}
      onFailure={this.loginFailure.bind(this)}
      onLogoutSuccess={this.logoutSuccess.bind(this)}
      isSignedIn={true}
    /></Nav>)

  }


}

class Header extends React.Component {

  constructor(props){
    super(props);
  }

  menuSelect(eventKey) {
    console.log("eventKey", eventKey);
    if(eventKey === PROFILE_MENU_ACTIONS.LOGOUT){
      console.log("logged out")
      return
    }
    this.props.root.changeView(eventKey);
  }

  render(){
    return (
      <Navbar
        inverse
        style={{margin:0}}
        onSelect={this.menuSelect.bind(this)}
      >
        <Navbar.Header>
          <Navbar.Brand style={{display: "flex", alignItems: "center"}} >
            <a href="#home">
              Triptracks
              <Image src="/favicon.ico" style={{width:35, marginTop: -7, float:"left", marginRight:5}} thumbnail/>
            </a>
          </Navbar.Brand>
        </Navbar.Header>
        <ProfileMenu />
      </Navbar>)
  }
}


export default Header;
