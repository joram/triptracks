import React from "react";
import routeStore from '../routeStore'
import {debounce} from "../utils";
import {Dropdown} from "semantic-ui-react";
import {withRouter} from "react-router-dom";


class RouteSearchBox extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            options: [],
        };
        this.searchChanged = debounce(this.searchChanged, 250)
    }

    searchChanged(data){
        let search_text = data.target.value;
        routeStore.getRoutesBySearch(search_text).then(results => {
            let options = [];
            results.forEach(route => {
                options.push({
                    key: route.pubId,
                    text: route.name,
                    value: route.pubId,
                    image: { avatar: true, src: route.sourceImageUrl },
                });
            });
            let state = this.state;
            state.options = options;
            this.setState(state);
        })

    }

    onRouteSelect(data, {value}){
        this.props.history.push(`/route/${value}`);
    }

    render(){
        return <Dropdown
            button
            className='icon'
            // floating
            labeled
            icon='world'
            options={this.state.options}
            search
            text='Search Routes...'
            onSearchChange={this.searchChanged.bind(this)}
            onChange={this.onRouteSelect.bind(this)}
        />
    }
}
export default withRouter(RouteSearchBox);
