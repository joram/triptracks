import React from "react";
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import routeStore from '../routeStore'
import {Menu, Input, Image, Dropdown} from "semantic-ui-react";


class Header extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      isLoggedIn: false
    }
  }

  loginSuccess(resp) {
    console.log("login success ",resp);
    routeStore.createUser(resp);
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

  render(){

    let profile_menu = <Menu.Item position="right">
      <GoogleLogin
        clientId="965794564715-ebal2dv5tdac3iloedmnnb9ph0lptibp.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={this.loginSuccess.bind(this)}
        onFailure={this.loginFailure.bind(this)}
        onLogoutSuccess={this.logoutSuccess.bind(this)}
        isSignedIn={true}
      />;
    </Menu.Item>;
    if (this.state.isLoggedIn) {
      let trigger = <div>
        <Image style={{marginBottom: 0}} src={this.state.googleData.profileObj.imageUrl} size="mini" floated="left" circular/>
        <span style={{position:"relative", top:"8px"}}>{this.state.googleData.profileObj.name}</span>
      </div>;

      profile_menu =
        <Dropdown item trigger={trigger} className="align right">
          <Dropdown.Menu>
            <Dropdown.Item>My Routes</Dropdown.Item>
            <Dropdown.Item>My Plans</Dropdown.Item>
            <Dropdown.Item>Settings</Dropdown.Item>
            <Dropdown.Item>
              <a href="https://exp-shell-app-assets.s3.us-west-1.amazonaws.com/android/%40joram87/triptracks-143a3419688a427bbe352a8a35a99142-signed.apk">Android App</a>
            </Dropdown.Item>
            <Dropdown.Item>
              <GoogleLogout
                buttonText="Logout"
                onLogoutSuccess={this.logoutSuccess.bind(this)}
                render={renderProps => (<div onClick={renderProps.onClick}>Logout</div>)}
              />
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
    }



    return (
      <Menu inverted={true} compact style={{width: "100%", borderRadius:0}}>
        <Menu.Item name='home' style={{color: "#AAAAAA", fontSize:"28px", padding:5}}>
          <Image src="/favicon.ico" size="mini" floated="left"/>
          Triptracks
        </Menu.Item>

        <Menu.Item >
          <Input icon='search' placeholder='Search...' />
        </Menu.Item>

        {profile_menu}
      </Menu>
    )
  }
}


export default Header;
