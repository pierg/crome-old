import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../../assets/styles/tailwind.css";


export default function WorldModeling ({
    firstCategory,
    secondCategory,
    thirdCategory

}) {
    return (
        <>
            <div className="container px-4 mx-auto pt-16  ">
                <div className="flex flex-wrap">
                    <div className="w-full px-4 flex-1">

                    </div>
                    <div className="w- px-12 pt-20  flex-1 rounded border border-solid border-blueGray-100">
                        Environment div
                    </div>
                    <div className="w-full px-4 flex-1">

                    </div>
                </div>
            </div>
            <section className="mt- pt-24 pb-6 relative">
                <div className="container px-12 mx-full ">
                    <div className="flex flex-wrap">
                        <div className="pt-12 ">
                            <h2 className="text-4xl font-normal leading-normal mt-0 mb-2">
                                {firstCategory}
                            </h2>
                        </div>
                        <div className= "px-12">
                        </div>
                        <div
                            className="w-full flex-1 ">
                            <button
                                className="text-white px-12 py-16 bg-lightBlue-600 border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button"
                            >
                                <i className="fas fa-plus"/>
                            </button>
                        </div>
                    </div>
                </div>
            </section>
            <section className="mt- relative">
                <div className="container px-12 mx-full border-b border-blueGray-600 ">
                </div>
            </section>
            <section className="mt- pt-8 pb-6 relative">
                <div className="container px-12 mx-full ">
                    <div className="flex flex-wrap">
                        <div className="pt-12 ">
                            <h2 className="text-4xl font-normal leading-normal mt-0 mb-2">
                                {secondCategory}
                            </h2>
                        </div>
                        <div className= "px-12">
                        </div>
                        <div
                            className="w-full flex-1">
                            <button
                                className="text-white px-12 py-16 bg-lightBlue-600 border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button"
                            >
                                <i className="fas fa-plus"/>
                            </button>
                        </div>
                    </div>
                </div>
            </section>
            <section className="mt- pt-8 relative">
                <div className="container px-12 mx-full border-b border-blueGray-600 ">
                </div>
            </section>
            <section className="mt- pt-16 relative">
                <div className="container px-12 mx-full ">
                    <div className="flex flex-wrap">
                        <div className="pt-12 ">
                            <h2 className="text-4xl font-normal leading-normal mt-0 mb-2">
                                {thirdCategory}
                            </h2>
                        </div>
                        <div className= "px-12">
                        </div>
                        <div
                            className="w-full flex-1">
                            <button
                                className="text-white px-12 py-16 bg-lightBlue-600 border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button"
                            >
                                <i className="fas fa-plus"/>
                            </button>
                        </div>
                    </div>
                </div>
            </section>
        </>
    );
}
