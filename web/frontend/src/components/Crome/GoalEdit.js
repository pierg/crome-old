import React from 'react';
import {Button, ModalFooter} from "reactstrap";
import Input from "../Elements/Input";
import Checkbox from "../Elements/Checkbox";

function GoalEdit(props) {

    const [goal] = React.useState(JSON.parse(JSON.stringify(props.goal)));

    function changeParameter(e) {
        switch (e.target.name) {
            case "name": goal.name = e.target.value; break;
            case "description": goal.description = e.target.value; break;
            case "context-day": case "context-night" : goal.context = writeContext(e.target.name); break;
            default: break;
        }
        props.edit(goal)
    }

    function parseContext(context) {
        return context === undefined ? ["",""] : [context.includes("day") ? "checked" : "", context.includes("night") ? "checked" : ""]
    }

    function writeContext(context) {
        let day = goal.context === undefined ? false : goal.context.includes("day")
        let night = goal.context === undefined ? false : goal.context.includes("night")
        context === "context-day" ? day ? day = false : day = true : night ? night = false : night = true
        return day ? night ? ["day", "night"] : ["day"] : night ? ["night"] : undefined
    }

    return(
        <>
            <div className="modal-header justify-content-center">
                <button
                    aria-hidden={true}
                    className="close"
                    onClick={props.close}
                    type="button"
                >
                    <i className="now-ui-icons ui-1_simple-remove"/>
                </button>
                <h4 className="title title-up">Edit a Goal</h4>
            </div>
            <div className="modal-body justify-content-center">
                <Input type="text" placeholder="Name" name="name" value={goal.name} onChange={changeParameter}/>
                <Input type="textarea" placeholder="Description" name="description" value={goal.description} onChange={changeParameter}/>
                <Checkbox label="Day" name="context-day" checked={parseContext(goal.context)[0]} onChange={changeParameter}/>
                <Checkbox label="Night" name="context-night" checked={parseContext(goal.context)[1]} onChange={changeParameter}/>
            </div>
            <ModalFooter>
                <Button color="danger" onClick={props.close}>
                    Cancel
                </Button>
                <Button color="info" onClick={() => props.save(goal)}>
                    Save
                </Button>
            </ModalFooter>
        </>
    );
}

export default GoalEdit;