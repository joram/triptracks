import React, { Component } from 'react';
import { Text, View } from 'react-native';
import RoutesMap from "./src/routes_map";


class TriptracksApp extends Component {

    render() {
        return (<>
            <RoutesMap/>
            <View style={{position:'absolute', backgroundColor: 'red', top: 150, width: "100%"}}>
                {/*<Text>{this.state.msg}</Text>*/}
                <Text>no message for now</Text>
            </View>
        </>);

    }
}


export default TriptracksApp;