import React from 'react';
import './App.css';
import Header from "./components/header";
import Home from "./components/views/home";
import Footer from "./components/footer";
import APIClient from "./api-client/client";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Settings from "./components/views/settings";
import MyRoutes from "./components/views/my_routes";
import MyPlans from "./components/views/my_plans";
import CreatePlan from "./components/views/create_plan";
import EditPlan from "./components/views/edit_plan";
import MyPackingLists from "./components/views/my_packing_lists";
import CreatePackingList from "./components/views/create_packing_list";

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
            this.setState({
                route: route,
                pub_id: route.pub_id,
            })
        });
    }

    render() {
        let home = <Home route={this.state.route} onRouteSelect={this.onRouteSelect.bind(this)}/>;
        return <BrowserRouter>
                <Header onRouteSelect={this.onRouteSelect.bind(this)}/>
                <Route exact path="/" render={() => home}/>
                <Route exact path={`/route/:pub_id`} render={() => home}/>
                <Route exact path="/settings" component={Settings}/>
                <Route exact path="/routes" render={() =>
                    <MyRoutes
                        googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&key=AIzaSyANDvIT7YDXDjP-LW0bFRdoFwm9QeL9q1g"
                        loadingElement={<div id="map_loading_element" />}
                        containerElement={<div id="map_container" />}
                        mapElement={<div id="map_element" />}
                        onRouteSelect={this.onRouteSelect.bind(this)} />
                }/>
                <Route exact path="/plans" component={MyPlans} />
                <Route exact path="/packing_lists" component={MyPackingLists} />
                <Route exact path="/packing_list/create" component={CreatePackingList} />
            <Switch>
                <Route exact path="/plan/create" component={CreatePlan} />
                <Route exact path={`/plan/:pub_id`} component={EditPlan} />
            </Switch>
            <Footer/>
        </BrowserRouter>
    }
}

export default App;
