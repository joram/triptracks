import React from 'react';
import './App.css';
import Header from "../../web/src/components/header";
import Home from "../../web/src/components/views/home";
import Footer from "../../web/src/components/footer";
import routeStore from "../../web/src/api-client/routeStore";
import {BrowserRouter, Route} from "react-router-dom";
import Settings from "../../web/src/components/views/settings";
import MyRoutes from "../../web/src/components/views/my_routes";

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
        routeStore.getRouteByID(pubId).then(route => {
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
