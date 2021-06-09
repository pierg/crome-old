import React from 'react';
import {Button, ModalFooter} from "reactstrap";
import Input from "../Elements/Input";
import Checkbox from "../Elements/Checkbox";
import ContractContentEditor from "../Custom/ContractContentEditor";
import contracteditorinfo from "_texts/custom/contracteditorinfo.js";
import makeListOf from "hooks/stringToListConversion.js";

function GoalEdit(props) {

    const [goal] = React.useState(JSON.parse(JSON.stringify(props.goal)));

    function changeParameter(e, contractType = false, index = 0, propValue = false, subKey = -1) {
        const value = propValue || e.target.value
        const contractTypeIndex = contractType ? goal.contract[contractType][index] : false
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

    function deleteContractContent(key, contractType) {
        goal.contract[contractType].splice(key, 1)
        props.edit(goal)
    }

    function addContractContent(contractType, key = -1) {
        goal.contract[contractType].push({ltl_value: ""})
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
                    <i className={props.info.modal.close}/>
                </button>
                <h4 className="title title-up">{props.info.title}</h4>
            </div>
            <div className="modal-body justify-content-center">
                <Input type="text" placeholder="Name" name="name" value={goal.name} onChange={changeParameter}/>
                <Input type="textarea" placeholder="Description" name="description" value={goal.description} onChange={changeParameter}/>
                <Checkbox label="Day" name="context-day" checked={parseContext(goal.context)[0]} onChange={changeParameter}/>
                <Checkbox label="Night" name="context-night" checked={parseContext(goal.context)[1]} onChange={changeParameter}/>
                {props.info.contract.map((prop, key) => (
                    <><h4 className="title title-up">{prop.title}</h4>
                    <ContractContentEditor
                        items={goal.contract[prop.title]}
                        patterns={props.patterns}
                        color={prop.color}
                        changeParameter={changeParameter}
                        deleteContent={deleteContractContent}
                        addContent={addContractContent}
                        contractType={prop.title}
                        {...contracteditorinfo}/></>
                ))}
            </div>
            <ModalFooter>
                <Button color={props.info.modal.cancelColor} onClick={props.close}>
                    {props.info.modal.cancelText}
                </Button>
                <Button color={props.info.modal.saveColor} onClick={() => props.save(goal)}>
                    {props.info.modal.saveText}
                </Button>
            </ModalFooter>
        </>
    );
}

export default GoalEdit;