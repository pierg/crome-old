import React from 'react';
import Checkbox from "../Elements/Checkbox";
import ContractAccordionItem from "./ContractAccordionItem";

function GoalView(props) {

    const contract = []
    const [open, setOpen] = React.useState();

    for (const property in props.contract) {
        contract[Object.keys(props.contract).indexOf(property)] = []
        contract[Object.keys(props.contract).indexOf(property)]["title"]=property
        contract[Object.keys(props.contract).indexOf(property)]["content"]=props.contract[property]
    }

    function parseContext(context) {
        return context===undefined ? ["",""] : [context.includes("day") ? "checked" : "", context.includes("night") ? "checked" : ""]
    }

    let callBackAction = (key) => {
      setOpen(key);
    };

    return(
        <div className={"w-full lg:w-6/12 xl:w-5/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-white rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out"}>
            <div className="flex-auto p-4 pr-0">
                <div className="flex">
                    <div className="flex flex-wrap">
                        <div className="flex flex-wrap">
                            <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                                <span className="font-bold text-xl uppercase text-blueGray-700">{props.title}</span>
                            </div>
                        </div>
                        <div className="flex flex-col flex-wrap w-full">
                            <div className="relative w-full pr-4 mb-4 max-w-full flex-grow flex-1">
                                <span className="text-md text-blueGray-700">
                                    {props.description}
                                </span>
                            </div>
                            <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                                <Checkbox className="mr-4" label="Day" readOnly checked={parseContext(props.context)[0]}/>
                                <Checkbox label="Night" readOnly checked={parseContext(props.context)[1]}/>
                            </div>
                            {contract.map((prop, key) => (
                                <div key={key} className="relative w-full pr-4 max-w-full flex-grow flex-1">
                                    <div
                                        className="overflow-hidden relative flex flex-col min-w-0 break-words bg-white w-full border-b border-blueGray-200">
                                        <ContractAccordionItem
                                            title={prop.title[0].toUpperCase() + prop.title.slice(1)}
                                            content={prop.content}
                                            patterns={props.patterns}
                                            color={"lightBlue"}
                                            setOpen={() => callBackAction(key)}
                                            number={key}
                                            defaultOpened={key === open}/>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="flex flex-wrap min-content">
                        <div className="relative pl-4 flex justify-end flex-initial">
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
                        <div className="relative pl-4 flex justify-end items-end flex-initial">
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
            </div>
    </div>);
}

export default GoalView;