import React from 'react';
import './App.css';
import Header from "./components/header";
import Home from "./components/views/home";
import Footer from "./components/footer";
import { BrowserRouter, Route } from "react-router-dom";

class App extends React.Component {
    render(){
        return <>
            <BrowserRouter>
                <Header/>
                <Route exact path="/" render={(props) => <Home/>} />
                <Footer/>
            </BrowserRouter>
        </>
    }
}

export default App;
