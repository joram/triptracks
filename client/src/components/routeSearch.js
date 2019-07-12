import React from "react";
import history from "../history";
import {FormControl, Nav} from "react-bootstrap";
import routeStore from '../routeStore'

function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}


class RouteSearchResult extends React.Component {

    handleClick(e) {
        history.push(`/?route=${this.props.route.pubId}&bbox=${this.props.route.bounds.toUrlValue()}`);
        this.props.parent.resultClicked()
    }

    render() {
        return (
            <div>
                <i onClick={this.handleClick.bind(this)}>{this.props.route.name}</i>
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

    resultClicked() {
        this.state.show = false;
        this.forceUpdate()
    }

    render() {
        if (this.props.results.length === 0 || !this.state.show) {
            return null
        }

        let result_lis = this.props.results.map((route) =>
            <RouteSearchResult key={route.pubId} route={route} parent={this}/>
        );
        return (
            <div style={{
                position: "absolute",
                zIndex: 99,
                color: "#33",
                backgroundColor: "white",
                width: "300px",
                marginTop: "34px",
            }} className="rounded-bottom">
                <ul>
                    {result_lis}
                </ul>
            </div>
        )
    }
}

class RoutesSearch extends React.Component {

    search = debounce(function () {
        routeStore.getRoutesBySearch(this.state.searchText);
    }, 200);

    constructor(props) {
        super(props);
        this.state = {
            results: [],
            searchText: null,
        };
        routeStore.subscribeGotSearch(this.gotResults.bind(this))
    }

    gotResults(data) {
        if (data.search_text !== this.state.searchText) {
            return
        }
        this.setState({
            results: routeStore.getRoutesBySearch2(data.search_text)
        })

    }

    handleChange(e) {
        let searchText = e.target.value;
        this.state.searchText = searchText;
        this.setState({results: []});
        if (searchText.length < 3) {
            return
        }
        this.search(searchText);
    }

    render() {
        return (
            <Nav style={{margin: "auto"}}>
                <FormControl
                    style={{width: "300px"}}
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
