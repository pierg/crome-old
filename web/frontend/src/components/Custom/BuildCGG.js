import React from 'react';
import Checkbox from "../Elements/Checkbox";
import Radio from "../Elements/Radio";
import Button from "../Elements/Button";

function BuildCGG(props) {

    function changeOperator(operator) {
        props.setOperator(operator)
    }

    function changeGoals(goal) {
        let tmpSelectedGoals = JSON.parse(JSON.stringify(props.selectedGoals))
        tmpSelectedGoals.includes(goal) ? tmpSelectedGoals.splice(tmpSelectedGoals.indexOf(goal), 1) : tmpSelectedGoals.push(goal)
        props.updateSelectedGoals(tmpSelectedGoals)
    }

    return(
        <>
            <div className="w-full flex justify-center my-4">
                {props.infos.operators.map((prop, key) => (
                    <Radio key={key} label={prop} onChange={() => changeOperator(prop)} checked={props.selectedOperator === prop} name="operator"/>
                ))}
            </div>
            <div className="flex">
                <div className="w-1/2 flex flex-col">
                    {props.cgg !== null && props.cgg.nodes.map((prop, key) => (
                        <Checkbox key={key} onChange={() => changeGoals(prop.id)} checked={props.selectedGoals.includes(prop.id) ? "checked" : ""} label={prop.hasOwnProperty("name") ? prop.name : props.findGoalById(prop.id)["name"]}/>
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

