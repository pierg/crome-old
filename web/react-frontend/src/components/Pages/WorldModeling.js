import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";

export default function WorldModeling ({

}) {
    return (
        <>
            <div className="container px-4 mx-auto pt-24 ">
                <div className="flex flex-wrap">
                    <div className="w-full px-4 flex-1"/>
                    <div className="w- px-12 pt-20  flex-1 rounded border border-solid border-blueGray-100">
                        Environment div
                    </div>
                    <div className="w-full px-4 flex-1"/>
                </div>
            </div>
            <section className="mt- md:mt-40 pt-20 relative">
                <div className="container px-12 mx-full ">
                    <div className="flex flex-wrap">
                        <div className="pt ">
                            <h2 className="text-4xl font-normal leading-normal mt-0 mb-2">
                            Actions
                            </h2>
                        </div>
                        <div className= "px-12">
                        </div>
                        <div class="Actions"
                            className="w-full flex-1 rounded border border-solid border-blueGray-100">
                            <button class="Actions"
                                className="text-white px-12 py-16 bg-lightBlue-600 border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button"
                            onclick="addAction(0)">
                                <i className="fas fa-plus"/>
                        </button>
                        </div>
                    </div>
                </div>
            </section>
        </>
    );
}
