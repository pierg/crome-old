import React from "react";

const ChildComponent = props => <div className="w-full lg:w-6/12 xl:w-3/12 m-4 px-4 relative flex flex-col min-w-0 break-words bg-white rounded mb-6 xl:mb-0 shadow-lg">
    <div className="flex-auto p-4">
        <div className="flex flex-wrap">
            <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                <span className="font-bold text-xl uppercase text-blueGray-700">
                {props.statTitle + " " + props.number}
              </span>
            </div>
            <div className="relative w-auto pl-4 flex-initial">
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
                {props.statDescription}
              </span>
            </div>
            <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
                <span className="font-bold text-xs text-blueGray-700">
                {props.statContext}
              </span>
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
</div>;

export default ChildComponent;