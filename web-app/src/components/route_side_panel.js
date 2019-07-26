import React from "react";
import {Image, Header, Container, ButtonGroup, Button, Icon} from "semantic-ui-react";
import routeStore from "../api-client/routeStore"


class Route_side_panel extends React.Component {

    render() {
        if(this.props.route === null){
            return null
        }
        return <>
            <Header textAlign="center" style={{paddingTop:"5px"}}>{this.props.route.name}</Header>
            <ButtonGroup>
                <Button onClick={this.toggleFavourite.bind(this)}><Icon name="heart"/></Button>
            </ButtonGroup>
            <Image src={this.props.route.sourceImageUrl} alt="Route" style={{width: "100%", padding: "5px"}}/>
            <Container>
                {this.props.route.description}
            </Container>
        </>
    }

    toggleFavourite(){
        routeStore.addToBucketList(this.props.route.pubId);
    }
}

export default Route_side_panel;