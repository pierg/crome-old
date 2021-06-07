import React from 'react';
import {Button, ModalFooter} from "reactstrap";
import Input from "../Elements/Input";
import Checkbox from "../Elements/Checkbox";
//import CustomTable from "../NowUI/CustomTable";
import ContractContentEditor from "../Custom/ContractContentEditor";

function GoalEdit(props) {

    const [goal] = React.useState(JSON.parse(JSON.stringify(props.goal)));

    function changeParameter(e, assumptions = false, index = 0, propValue = false, subKey = -1) {

        const value = propValue || e.target.value
        const contractTypeIndex = assumptions ? goal.contract.assumptions[index] : goal.contract.guarantees[index]
        switch (e.target.name) {
            case "name": goal.name = value; break;
            case "description": goal.description = value; break;
            case "context-day": case "context-night" : goal.context = writeContext(e.target.name); break;
            case "ltl_value": contractTypeIndex.ltl_value = value; break;
            case "contentName": contractTypeIndex.pattern.name = value; break;
            case "type": if(value === "Pattern") { contractTypeIndex.pattern={name: "", arguments: []} } else { delete contractTypeIndex.pattern } break;
            case "subValue": contractTypeIndex.pattern.arguments[subKey] = {"value": makeListOf(value)}; break;
            default: break;
        }
        props.edit(goal)
    }

    function deleteContractContent(key, assumptions) {
        assumptions ? goal.contract.assumptions.splice(key, 1) : goal.contract.guarantees.splice(key, 1)
        props.edit(goal)
    }

    function addContractContent(assumptions, key = -1) {
        assumptions ? goal.contract.assumptions.push({ltl_value: ""}) : goal.contract.guarantees.push({ltl_value: ""})
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
                <h4 className="title title-up">Assumptions</h4>
                <ContractContentEditor
                    items={goal.contract.assumptions}
                    patterns={props.patterns}
                    color="lightBlue"
                    changeParameter={changeParameter}
                    deleteContent={deleteContractContent}
                    addContent={addContractContent}
                    assumptions={true}/>
                <h4 className="title title-up">Guarantees</h4>
                <ContractContentEditor
                    items={goal.contract.guarantees}
                    patterns={props.patterns}
                    color="lightBlue"
                    changeParameter={changeParameter}
                    deleteContent={deleteContractContent}
                    addContent={addContractContent}
                    assumptions={false}/>
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

function makeListOf(str) {
    if (Array.isArray(str)) return str

    let list = [""]
    let index = 0
    for (let i=0; i<str.length; i++) {
        if (str[i] === ",") {
           index++
           list[index] = ""
           if (i !== str.length - 1 && str[i+1] === " ") {
                i++
           }
        }
        else list[index] += str[i]
    }
    return index === 0 ? list[0] : list
}