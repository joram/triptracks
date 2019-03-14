import React from "react";


class RouteDetails extends React.Component {

  constructor(props) {
    super(props);
    this.state = {route: []}
  //  todo: register for emits, and on url change, ask for route details
  }

  render() {

    let style = {
      left:"0",
      width: "300px",
      border: "solid thin black",
      height: `${window.innerHeight}px`,
      overflow: "hidden",
      textOverflow: "ellipsis",
      position: "absolute",
    };

    if(this.props.route === null) {
      return <div key="route_details" id="route_details" style={style}/>
    }

    return <div key="route_details" id="route_details" style={style}>
      <h3 style={{ width:"300px" }}>{this.state.route.name}</h3>
      {this.state.route.description}
    </div>
  }
}

export default RouteDetails;