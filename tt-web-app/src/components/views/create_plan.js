import React from "react";
import {Form, Input, Container, Button} from "semantic-ui-react";
import client from "../../api-client/client";
import {log_graphql_errors} from "../../api-client/utils";


class CreatePlan extends React.Component {

    pub_id = null;
    name = "";
    summary = "";
    start = null;
    end = null;

    onSave(){
        client.createOrUpdatePlan(
            this.pub_id,
            this.name,
            this.summary,
            this.start,
            this.end,
        ).then(data => {
            log_graphql_errors("create or update plan", data);
            console.log(data)
        })
    }

    onNameUpdate(e){ this.name = e.target.value; }
    onSummaryUpdate(e){ this.summary = e.target.value; }
    onStartUpdate(e){ this.start = e.target.value;}
    onEndUpdate(e){ this.end = e.target.value; }

    render() {
        return (<Container style={{paddingTop:"15px"}}>
            <Form>
                <Input
                    type="text"
                    name="name"
                    label="Name"
                    onChange={this.onNameUpdate.bind(this)}
                    defaultValue={this.name}
                    fluid
                />
                <br/>

                <Input
                    type="text"
                    name="summary"
                    label="summary"
                    onChange={this.onSummaryUpdate.bind(this)}
                    defaultValue={this.summary}
                    fluid
                />
                <br/>

                <Input
                    type="date"
                    name="start"
                    label="start"
                    onChange={this.onStartUpdate.bind(this)}
                    defaultValue={this.start}
                />
                <br/>
                <br/>

                <Input
                    type="date"
                    name="end"
                    label="end"
                    onChange={this.onEndUpdate.bind(this)}
                    defaultValue={this.end}
                />
                <br/>

                <Button floated="right" content="Save" onClick={this.onSave.bind(this)}/>
                <br/>
                <br/>

            </Form>
        </Container>);
    }
}

export default CreatePlan;