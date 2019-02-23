import React from "react";
import {Navbar, Nav, NavDropdown, MenuItem, Image, FormControl} from "react-bootstrap";
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import history from "../history";

const PROFILE_MENU_ACTIONS = {
  ROUTES: 0,
  PLANS: 1,
  SETTINGS: 2,
  LOGOUT: 3,
};

function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

function log_graphql_errors(data){
  if(data.errors !== undefined){
    data.errors.forEach(function(err){
      console.log("error: ",err.message);
    });
  }
}

class RouteSearchResult extends React.Component {

  render() {
    return (
      <div>
        <i onClick={this.handleClick.bind(this)} >{this.props.name}</i>
        <br/>
      </div>
    )
  }

  handleClick(e){history.push(`/?route=${this.state.pubId}&bbox=${this.state.bbox.toUrlValue()}`)}


}

class RouteSearchResults extends React.Component {

  render() {
    if(this.props.results.length === 0) {
      return null
    }

    let result_lis = this.props.results.map((result) =>
      <RouteSearchResult key={result.pubId}  pubId={result.pubId} name={result.name} />
    );
    return (
      <div style={{
        position: "absolute",
        zIndex: 99,
        color: "#33",
        backgroundColor: "white",
        width: "300px",
        marginTop:"34px",
      }} className="rounded-bottom">
      <ul>
        {result_lis}
      </ul>
      </div>
    )
  }
}

class RoutesSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      results: [],
    }

    this.url = "https://app.triptracks.io/graphql";
    if(window.location.hostname==="localhost"){
      this.url = "http://127.0.0.1:8000/graphql";
    }

  }

  search = debounce(function (searchtext){
    console.log("searching for ", searchtext);

    // cleared search
    if(searchtext === ""){
      this.setState({
        results: []
      });
      return
    }

    let query = `
      query route_search {
        routesSearch(searchText:"${searchtext}"){
          pubId
          name
        }
      }
    `;

    let body = JSON.stringify({query});
    return fetch(this.url, {
      method: 'POST',
      mode: "cors",
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: body
    })
    .then(r => r.json())
    .then(data => {
      log_graphql_errors(data);
      this.setState({
        results: data.data.routesSearch
      });
      console.log(this.state)
    });

  }, 200);

  handleChange(e){
    this.search(e.target.value);
  }

  render() {
    return (
      <Nav  style={{margin:"auto"}}>
          <FormControl
            style={{ width:"300px"}}
            type="text"
            placeholder="Search Routes"
            className="mr-sm-2"
            id="routes_search"
            onChange={this.handleChange.bind(this)}
          />
          <RouteSearchResults results={this.state.results}/>
      </Nav>
    )
  }
}

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
          <a href="#home" style={{color: "#AAAAAA"}}>
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
