import React from "react";
import {Image, Header, Container, ButtonGroup, Button, Icon} from "semantic-ui-react";
import client from "../api-client/client"
import {url} from "../api-client/utils"
import {Link} from "react-router-dom";

class Route_side_panel extends React.Component {

    render() {
        if(this.props.route === null){
            return null
        }

        let download_url = url.replace("/graphql", "")+"/route/"+this.props.route.pubId+"/gpx";

        return <>
            <Header textAlign="center" style={{paddingTop:"5px"}}>{this.props.route.name}</Header>
            <ButtonGroup>
                <Button onClick={this.toggleFavourite.bind(this)}><Icon name="heart"/></Button>
                <Button as="a" href={download_url} target="_blank">
                    <Icon name="download"/>
                </Button>
            </ButtonGroup>
            <Image src={this.props.route.sourceImageUrl} alt="Route" style={{width: "100%", padding: "5px"}}/>
            <Container>
                {this.props.route.description}
            </Container>
        </>
    }

    toggleFavourite(){
        client.addToBucketList(this.props.route.pubId);
    }

    downloadGPX(){
        console.log("downloading gpx for", this.props.route.pubId);
        client.downloadGPXcontent().then(data => {
            console.log(data);
        })
    }
}

export default Route_side_panel;