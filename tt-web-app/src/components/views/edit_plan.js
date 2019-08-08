import client from "../../api-client/client";
import CreatePlan from "./create_plan";


class EditPlan extends CreatePlan {

    constructor(props){
        super(props);
        let pub_id = props.match.params.pub_id;
        client.getTripPlan(pub_id).then(plan => {
            let start = "";
            if(plan.startDatetime){
                start = plan.startDatetime.split("T")[0];
            }

            let end = ""
            if(plan.endDatetime){
                end = plan.endDatetime.split("T")[0];
            }

            this.pub_id = plan.pubId;
            this.name = plan.name;
            this.summary = plan.summary;
            this.start = start;
            this.end = end;
            this.forceUpdate()
        });
    }
}

export default EditPlan;