import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";

export default function Index ({

}) {
    return (
        <>
            <div>
                <h1 className="text-6xl font-normal leading-normal mt-0 mb-2 text-indigo-800">
                Contract-Based Goals Graph
                </h1>
            </div>
            <div className="container px-4 mx-auto">
                <div className="flex flex-wrap">
                    <div className="w-full px-4 flex-1 rounded border border-solid border-blueGray-100">
                      <span className="text-sm block my-4 p-3 text-blueGray-700">Create your own CGG with customized goals, actions, locations...</span>
                      <button className="text-indigo-500 bg-transparent border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-indigo-600 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">
                          <i className="fas fa-upload"></i> Create CGG
                      </button>
                    </div>
                    <div className="w-full px-4 flex-1">

                    </div>
                        <div className="w-full px-4 flex-1 rounded border border-solid border-blueGray-100">
                      <span className="text-sm block my-4 p-3 text-blueGray-700 ">Load an existing example of CGG</span>
                      <button className="text-indigo-500 bg-transparent border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-indigo-600 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">
                          <i className="fas fa-plus-circle"></i> Load CGG
                      </button>
                    </div>
                </div>
            </div>
        </>
    );
}
