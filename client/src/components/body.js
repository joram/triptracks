import React from "react";
import Home from "./views/home";
// import Settings from "./views/settings"
// import 'semantic-ui-css';

class Body extends React.Component {

    render() {
        return <Home/>;

        if (this.props.view === "settings"){
            // return (<Settings/>);
            return null
        }
    }
}


export default Body;