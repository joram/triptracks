import React from "react";
import {GoogleLogin, GoogleLogout} from 'react-google-login';
import routeStore from '../routeStore'
import {Dropdown, Image, Input, Menu} from "semantic-ui-react";
import { Link } from "react-router-dom";


class Header extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoggedIn: false
        }
    }

    loginSuccess(resp) {
        console.log("login success ", resp);
        routeStore.createUser(resp);
        this.setState({
            isLoggedIn: true,
            googleData: resp,
        })
    }

    loginFailure(resp) {
        console.log("failed login ", resp);
        this.setState({isLoggedIn: false})
    }

    logoutSuccess(resp) {
        console.log("logout success ", resp);
        this.setState({isLoggedIn: false})
    }

    render() {

        let profile_menu = <Menu.Item position="right">
            <GoogleLogin
                clientId="965794564715-ebal2dv5tdac3iloedmnnb9ph0lptibp.apps.googleusercontent.com"
                buttonText="Login"
                onSuccess={this.loginSuccess.bind(this)}
                onFailure={this.loginFailure.bind(this)}
                onLogoutSuccess={this.logoutSuccess.bind(this)}
                isSignedIn={true}
            />
        </Menu.Item>;
        if (this.state.isLoggedIn) {
            let trigger = <div>
                <Image style={{marginBottom: 0}} src={this.state.googleData.profileObj.imageUrl} size="mini"
                       floated="left" circular/>
                <span style={{position: "relative", top: "8px"}}>{this.state.googleData.profileObj.name}</span>
            </div>;

            let link_style = {color:"rgba(0,0,0,.87)"};
            profile_menu =
                <Dropdown item trigger={trigger} className="align right">
                    <Dropdown.Menu inverted >
                        <Dropdown.Item><Link to="/routes" style={link_style}>My Routes</Link></Dropdown.Item>
                        <Dropdown.Item><Link to="/plans" style={link_style}>My Plans</Link></Dropdown.Item>
                        <Dropdown.Item><Link to="/settings" style={link_style}>Settings</Link></Dropdown.Item>
                        <Dropdown.Item>
                            <a href="/mobile_app/android/triptracks-v1.0.0.apk" style={link_style}>Download
                                App</a>
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
            <Menu inverted={true} compact style={{width: "100%", borderRadius: 0}}>
                <Link to="/">
                    <Menu.Item name='home' style={{color: "#AAAAAA", fontSize: "26px", paddingTop:10, paddingLeft:3, paddingBottom:0}}>
                        <Image src="/favicon.ico" size="mini" floated="left"/>
                        Triptracks
                    </Menu.Item>
                </Link>

                <Menu.Item>
                    <Input icon='search' placeholder='Search...'/>
                </Menu.Item>
                {profile_menu}
            </Menu>
        )
    }
}


export default Header;
