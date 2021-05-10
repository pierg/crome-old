import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";

export default function Index ({

}) {
    return (
        <>
            <div className="container px-4 mx-auto pt-24 ">
                <div className="flex flex-wrap">
                    <div className="w-full px-4 flex-1">

                    </div>
                <h1 className="text-5xl font-normal leading-normal mt-0 mb-2 text-lightBlue-600">
                Contract-Based Goals Graph
                </h1>
                        <div className="w-full px-4 flex-1">

                    </div>

            </div>
            </div>
            <section className="mt-48 md:mt-40 pb-48 pt-48 relative">
            <div className="container px-0 mx-auto ">
                <div className="flex flex-wrap">
                    <div className="w-full px-12 pt-20 flex-1 rounded border border-solid border-blueGray-100">
                        <div> <h3 className="text-2xl mb-2 font-light leading-normal"> Create your own CGG with customized goals, actions, locations...</h3></div>

                        <div className="pt-6" ><button className="text-lightBlue-600 bg-transparent border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">
                          <i className="fas fa-upload"></i> Create CGG
                        </button></div>
                    </div>
                    <div className="w-full px-4 flex-1">

                    </div>
                        <div className="w-full px-12 pt-20 flex-1 rounded border border-solid border-blueGray-100">
                      <div><h3 className="text-2xl mb-2 pb-20 font-light leading-normal ">Load an existing example of CGG</h3></div>
                      <div className="pt-6"><button className="text-lightBlue-600 bg-transparent border border-solid border-indigo-500 hover:bg-indigo-500 hover:text-white active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">
                          <i className="fas fa-plus-circle"></i> Load CGG
                      </button></div>
                    </div>
                </div>
            </div>
            </section>
        </>
    );
}
