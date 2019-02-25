import React from "react";
import history from "../history";
import {FormControl, Nav} from "react-bootstrap";

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

  bbox(){
    let lines = JSON.parse(this.props.route.lines);
    let bounds = new google.maps.LatLngBounds();
    lines.forEach((line) => {
      line.forEach((coord) => {
        let lat = parseFloat(coord[0]);
        let lng = parseFloat(coord[1]);
        bounds.extend(new google.maps.LatLng({lat:lat, lng:lng}));
      })
    });
    return bounds
  }

  handleClick(e){
    history.push(`/?route=${this.props.route.pubId}&bbox=${this.bbox().toUrlValue()}`)
    this.props.parent.resultClicked()
  }

  render() {
    return (
      <div>
        <i onClick={this.handleClick.bind(this)} >{this.props.route.name}</i>
        <br/>
      </div>
    )
  }
}

class RouteSearchResults extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      show: true
    }
  }

  resultClicked(){
    this.state.show = false
    this.forceUpdate()
  }

  render() {
    if(this.props.results.length === 0 || !this.state.show) {
      return null
    }

    let result_lis = this.props.results.map((route) =>
      <RouteSearchResult key={route.pubId} route={route} parent={this} />
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
      searchText: null,
    }

    this.url = "https://app.triptracks.io/graphql";
    if(window.location.hostname==="localhost"){
      this.url = "http://127.0.0.1:8000/graphql";
    }

  }

  search = debounce(function (){
    console.log("searching for ", this.state.searchText);
    let searchtext = this.state.searchText;

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
          lines
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
      if(searchtext!==this.state.searchText){
        return
      }
      this.setState({
        results: data.data.routesSearch
      });
    });

  }, 200);

  handleChange(e){
    this.state.searchText = e.target.value;
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

export default RoutesSearch;
