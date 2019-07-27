import React from 'react';
import './App.css';
import Header from "./components/header";
import Home from "./components/views/home";
import Footer from "./components/footer";
import APIClient from "./api-client/client";
import {BrowserRouter, Route} from "react-router-dom";
import Settings from "./components/views/settings";
import MyRoutes from "./components/views/my_routes";

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            route: null,
        };

        let url_path = window.location.pathname;
        if (url_path.startsWith("/route/")) {
            let pubId = url_path.replace("/route/", "");
            this.onRouteSelect(pubId)
        }
    }

    onRouteSelect(pubId) {
        APIClient.getRouteByID(pubId).then(route => {
            if (route === null) {
                return
            }
            console.log(route);
            this.setState({
                route: route,
                pub_id: route.pub_id,
            })
        });
    }

    render() {
        let home = <Home route={this.state.route} onRouteSelect={this.onRouteSelect.bind(this)}/>;
        return <>
            <BrowserRouter>
                <Header onRouteSelect={this.onRouteSelect.bind(this)}/>
                <Route exact path="/" render={() => home}/>
                <Route exact path={`/route/:pub_id`} render={() => home}/>
                <Route exact path="/settings" component={Settings}/>
                <Route exact path="/routes" render={() => <MyRoutes onRouteSelect={this.onRouteSelect.bind(this)}/>}/>
                <Footer/>
            </BrowserRouter>
        </>
    }
}

export default App;
