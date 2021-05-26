import React from 'react';
import Checkbox from "../Elements/Checkbox";

function ChildComponent(props) {

    function parseContext(context) {
        return context===undefined ? ["",""] : [context.includes("day") ? "checked" : "", context.includes("night") ? "checked" : ""];
    }

    return(
    <div className="w-full lg:w-6/12 xl:w-5/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-white rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out">
        <div className="flex-auto p-4 pr-0">
            <div className="flex flex-wrap">
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                <span className="font-bold text-xl uppercase text-blueGray-700">
                {props.title}</span>
                </div>
                <div onClick={() => props.modify(true)} className="relative w-full pl-4 flex justify-end flex-initial">
                    <div
                        className={
                            "text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full " +
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
                    {/*<span className="font-bold text-xs text-blueGray-700">
                {props.statContext}
              </span>*/}
                    <Checkbox label="Day" readOnly checked={parseContext(props.context)[0]}/>
                    <Checkbox label="Night" readOnly checked={parseContext(props.context)[1]}/>
                </div>
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                <span className="font-bold text-xs text-blueGray-700">
                {props.statObjectives}
              </span>
                </div>
            </div>
            <div className="flex flex-wrap mt-16">
                <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                </div>
                <div className="relative w-auto pl-4 flex-initial">
                    <div
                        className={
                            "text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full " +
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

export default ChildComponent;