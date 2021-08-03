import React from 'react';
import Checkbox from "../Elements/Checkbox";
import Radio from "../Elements/Radio";
import Button from "../Elements/Button";

function BuildCGG(props) {

    const [refinementMessage, setRefinementMessage] = React.useState("")

    function changeOperator(operator) {
        if (operator === "Refinement" || props.selectedOperator === "Refinement") {
            operator === "Refinement" ? setRefinementMessage(props.infos.refinementMessages[0]) : setRefinementMessage("")
            props.updateSelectedGoals([])
        }
        props.setOperator(operator)
    }

    function changeGoals(goal) {

        let tmpSelectedGoals = JSON.parse(JSON.stringify(props.selectedGoals))

        if (props.selectedGoals.includes(goal)) { // Removing a goal
            if (props.selectedOperator === "Refinement") {
                setRefinementMessage(props.infos.refinementMessages[tmpSelectedGoals.length - 1])
            }
            tmpSelectedGoals.splice(tmpSelectedGoals.indexOf(goal), 1)
            props.updateSelectedGoals(tmpSelectedGoals)
        }
        else { // Adding a goal
            if (props.selectedOperator === "Refinement") {
                switch (tmpSelectedGoals.length) {
                    case 0: setRefinementMessage(props.infos.refinementMessages[1]); break;
                    case 1: setRefinementMessage(getGoalName(props.selectedGoals[0])+" --> "+getGoalName(goal)); break;
                    case 2: setRefinementMessage(props.infos.refinementMessages[2]); return;
                    default: break
                }
            }
            tmpSelectedGoals.push(goal)
            props.updateSelectedGoals(tmpSelectedGoals)
        }
    }

    function getGoalName(node) {
        if (node.hasOwnProperty("name")) {
            return node.name
        }
        else {
            return typeof node === "object" && node.hasOwnProperty("id") ? props.findGoalById(node.id)["name"] : props.findGoalById(node)["name"]
        }
    }

    return(
        <>
            <div className="w-full flex justify-center my-4">
                {props.infos.operators.map((prop, key) => (
                    <Radio key={key} label={prop} onChange={() => changeOperator(prop)} checked={props.selectedOperator === prop} name="operator"/>
                ))}
            </div>
            <div className="flex w-full justify-center">
                {refinementMessage}
            </div>
            <div className="flex">
                <div className="w-1/2 flex flex-col">
                    {props.cgg !== null && props.cgg.nodes.map((prop, key) => (
                        <Checkbox key={key} onChange={() => changeGoals(prop.id)} checked={props.selectedGoals.includes(prop.id) ? "checked" : ""} label={getGoalName(prop)}/>
                    ))}
                </div>
                <div className="w-1/2 flex justify-center items-center">
                    <Button onClick={props.applyOperator}>{props.infos.buttonText}</Button>
                </div>
            </div>
        </>
    );
}

export default BuildCGG;

