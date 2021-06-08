import React from 'react';
import {Button, ModalFooter} from "reactstrap";
import Input from "../Elements/Input";
import Checkbox from "../Elements/Checkbox";
import ContractContentEditor from "../Custom/ContractContentEditor";
import contracteditorinfo from "_texts/custom/contracteditorinfo.js";
import makeListOf from "hooks/stringToListConversion.js";

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
                    <i className={props.infos.modal.close}/>
                </button>
                <h4 className="title title-up">{props.infos.title}</h4>
            </div>
            <div className="modal-body justify-content-center">
                <Input type="text" placeholder="Name" name="name" value={goal.name} onChange={changeParameter}/>
                <Input type="textarea" placeholder="Description" name="description" value={goal.description} onChange={changeParameter}/>
                <Checkbox label="Day" name="context-day" checked={parseContext(goal.context)[0]} onChange={changeParameter}/>
                <Checkbox label="Night" name="context-night" checked={parseContext(goal.context)[1]} onChange={changeParameter}/>
                {/* TODO map */}
                <h4 className="title title-up">{props.infos.contract[0].title}</h4>
                <ContractContentEditor
                    items={goal.contract.assumptions}
                    patterns={props.patterns}
                    color={props.infos.contract[0].color}
                    changeParameter={changeParameter}
                    deleteContent={deleteContractContent}
                    addContent={addContractContent}
                    assumptions={true}
                    {...contracteditorinfo}/>
                <h4 className="title title-up">{props.infos.contract[1].title}</h4>
                <ContractContentEditor
                    items={goal.contract.guarantees}
                    patterns={props.patterns}
                    color={props.infos.contract[1].color}
                    changeParameter={changeParameter}
                    deleteContent={deleteContractContent}
                    addContent={addContractContent}
                    assumptions={false}
                    {...contracteditorinfo}/>
            </div>
            <ModalFooter>
                <Button color={props.infos.modal.cancelColor} onClick={props.close}>
                    {props.infos.modal.cancelText}
                </Button>
                <Button color={props.infos.modal.saveColor} onClick={() => props.save(goal)}>
                    {props.infos.modal.saveText}
                </Button>
            </ModalFooter>
        </>
    );
}

export default GoalEdit;