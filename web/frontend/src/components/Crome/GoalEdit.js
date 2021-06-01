import React from 'react';
import {Button, ModalFooter} from "reactstrap";
import Input from "../Elements/Input";
import Checkbox from "../Elements/Checkbox";

function GoalEdit(props) {



    const [goal] = React.useState(props.goal);

    function changeParameter(e) {
        props.check()
        switch (e.target.name) {
            case "name": goal.name = e.target.value; break;
            case "description": goal.description = e.target.value; break;
            case "context-day": case "context-night" : goal.context = writeContext(e.target.name); break;
            default: break;
        }

        props.save(goal)
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
            <Input type="text" placeholder="Name" name="name" value={goal.name} onChange={changeParameter}/>
            <Input type="text" placeholder="Description" name="description" value={goal.description} onChange={changeParameter}/>
            <Checkbox label="Day" name="context-day" checked={parseContext(goal.context)[0]} onChange={changeParameter}/>
            <Checkbox label="Night" name="context-night" checked={parseContext(goal.context)[1]} onChange={changeParameter}/>
            <ModalFooter>
                <Button color="default" type="button">
                    Nice Button
                </Button>
                <Button color="danger" onClick={props.close}>
                    Close
                </Button>
            </ModalFooter>
        </>
    );
}

export default GoalEdit;