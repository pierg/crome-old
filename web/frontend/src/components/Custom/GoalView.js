import React from 'react';
import Checkbox from "../Elements/Checkbox";
import ContractContentComponent from "./ContractContentComponent";

function GoalView(props) {

    const contract = []

    /*for (let i = 0; i < props.contract.length; i++) {
        contract[i] = []
        console.log(props.contract[i])
        for (const property in props.contract[i]) {
            console.log("prop")
            console.log(property)
            contract[i].push(<ContractContentComponent key={i*props.contract[i].length+j}
                type={contract[i][property].type}
                ltl_value={contract[i][property].ltl_value}
                content={contract[i][property].content}/>)
        }
    }*/

    for (const property in props.contract) {
        contract[Object.keys(props.contract).indexOf(property)] = []
        for (let i = 0; i < props.contract[property].length; i++) {
            contract[Object.keys(props.contract).indexOf(property)]["title"]=property
            contract[Object.keys(props.contract).indexOf(property)].push(<ContractContentComponent /*key={i*props.contract[i].length+j}*/
                type={props.contract[property][i].type}
                ltl_value={props.contract[property][i].ltl_value}
                content={props.contract[property][i].content}/>)
        }
    }

    function parseContext(context) {
        return context===undefined ? ["",""] : [context.includes("day") ? "checked" : "", context.includes("night") ? "checked" : ""]
    }

    return(
    <div className={"w-full lg:w-6/12 xl:w-5/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-white rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out"}>
        <div className="flex-auto p-4 pr-0">
            <div className="flex flex-wrap">
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                <span className="font-bold text-xl uppercase text-blueGray-700">
                {props.title}</span>
                </div>
                <div className="relative w-full pl-4 flex justify-end flex-initial">
                    <div
                        onClick={() => props.modify(true, props.number)}
                        className={
                            "text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full cursor-pointer " +
                            props.statIconColor
                        }
                    >
                        <i className={props.statIconName}/>
                    </div>
                </div>
            </div>
            <div className="flex flex-col flex-wrap">
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                    <span className="font-bold text-xs text-blueGray-700">
                        {props.description}
                    </span>
                </div>
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                    <Checkbox label="Day" readOnly checked={parseContext(props.context)[0]}/>
                    <Checkbox label="Night" readOnly checked={parseContext(props.context)[1]}/>
                </div>
                    {contract.map((prop, key) => (
                        <div key={key} className="relative w-full pr-4 max-w-full flex-grow flex-1">
                            <h2>{prop.title}</h2>
                        </div>
                    ))}
            </div>
            <div className="flex flex-wrap mt-16">
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1"/>
                <div className="relative w-auto pl-4 flex-initial">
                    <div
                        onClick={() => props.delete(props.number)}
                        className={
                            "text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full cursor-pointer " +
                            props.statIconColor
                        }
                    >
                        <i className={props.statSecondIconName}/>
                    </div>
                </div>
            </div>
        </div>
    </div>);
}

export default GoalView;