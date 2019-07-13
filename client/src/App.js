import React from 'react';
import './App.css';
import Header from "./components/header";
import Home from "./components/views/home";
import Footer from "./components/footer";
import routeStore from "./routeStore";
import { BrowserRouter, Route } from "react-router-dom";

class App extends React.Component {

    onRouteSelect(pubId){
        console.log("onRouteSelect", pubId);
        routeStore.getRouteByID(pubId).then(route => {
            console.log(route);
        });
    }

    render(){
        return <>
            <BrowserRouter>
                <Header onRouteSelect={this.onRouteSelect.bind(this)}/>
                <Route exact path="/" render={(props) => <Home/>} />
                <Route exact path={`/route/:pub_id`} render={(props) => <Home key={props.match.params.pub_id} pub_id={props.match.params.pub_id} />} />
                <Footer/>
            </BrowserRouter>
        </>
    }
}

export default App;
