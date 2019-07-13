import React from "react";
import routeStore from '../routeStore'
import {Image, Header, Container} from "semantic-ui-react";


class Route_side_panel extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            route: {
                name: "",
                sourceImageUrl: "",
                description: "",
            }
        };
        if(this.props.pub_id !== null){
            routeStore.getRouteByID(this.props.pub_id).then(route => {
                if(route !== null){
                    this.setState({route: route});
                }
            });
        }
    }

    render() {
        return <Container>
            <Header textAlign="center" style={{paddingTop:"5px"}}>{this.state.route.name}</Header>
            <Image src={this.state.route.sourceImageUrl} alt="Route" style={{width: "100%", padding: "5px"}}/>
            <Container>
            {this.state.route.description}
            </Container>
        </Container>
    }
}

export default Route_side_panel;