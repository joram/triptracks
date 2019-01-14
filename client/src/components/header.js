import React from "react";
import {Navbar, Nav, NavItem, NavDropdown, MenuItem, Image} from "react-bootstrap";

class MenuTitle extends React.Component {
  render() {
    return ("John Oram")
  }
}

class Menu extends React.Component {
  render() {
    if (this.props.isLoggedIn) {
      return (<Nav pullRight>
        <NavDropdown eventKey={3} title={<MenuTitle isLoggedIn={this.props.isLoggedIn} />} id="basic-nav-dropdown">
          <MenuItem eventKey={3.1}>Action</MenuItem>
          <MenuItem eventKey={3.2}>Another action</MenuItem>
          <MenuItem eventKey={3.3}>Something else here</MenuItem>
          <MenuItem divider/>
          <MenuItem eventKey={3.4}>Separated link</MenuItem>
        </NavDropdown>
      </Nav>)
    }
    return (<Nav pullRight>Please Login</Nav>)

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
        <Menu isLoggedIn={true} />
      </Navbar>)
  }
}


export default Header;
