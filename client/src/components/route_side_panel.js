import React from "react";
import {Image, Header, Container} from "semantic-ui-react";


class Route_side_panel extends React.Component {

    render() {
        return <Container>
            <Header textAlign="center" style={{paddingTop:"5px"}}>{this.props.route.name}</Header>
            <Image src={this.props.route.sourceImageUrl} alt="Route" style={{width: "100%", padding: "5px"}}/>
            <Container>
                {this.props.route.description}
            </Container>
        </Container>
    }
}

export default Route_side_panel;