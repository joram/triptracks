import React from 'react';
import './App.css';
import Header from "./components/header";
import Home from "./components/views/home";
import Footer from "./components/footer";
import routeStore from "./routeStore";
import { BrowserRouter, Route } from "react-router-dom";

class App extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            route: null,
        };

        let url_path = window.location.pathname;
        if(url_path.startsWith("/route/")){
            let pubId = url_path.replace("/route/", "");
            this.onRouteSelect(pubId)
        }
    }

    onRouteSelect(pubId){
        routeStore.getRouteByID(pubId).then(route => {
            this.setState(
                {
                    route: route,
                    pub_id: route.pub_id,
                }
            )
        });
    }

    render(){
        let home = <Home route={this.state.route} onRouteSelect={this.onRouteSelect.bind(this)} />;
        return <>
            <BrowserRouter>
                <Header onRouteSelect={this.onRouteSelect.bind(this)}/>
                <Route exact path="/" render={() => home} />
                <Route exact path={`/route/:pub_id`} render={() => home} />
                <Footer/>
            </BrowserRouter>
        </>
    }
}

export default App;
