import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import Sidebar from "../../../components/Sidebar/Sidebar";
import customsidebar from "../../../_texts/admin/sidebar/customsidebar";


export default function RunExample ({

}) {
    return (
        <>
            <Sidebar {...customsidebar} />
            <div className="relative md:ml-64 bg-blueGray-100">
                <form action="/createCGG/" method="post">
                    <select name="exampleButtons">
                        <option>0_modeling_goals</option>
                        <option>1_analysis_build_cgg</option>
                        <option>2_synthesis_realize_controllers</option>
                        <option>3_simulation_orchestrate</option>
                    </select>
                    <button className="text-lightBlue-600 bg-transparent border border-solid border-lightBlue-600 active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-4 ease-linear transition-all duration-150" type="button" name="submitExample" type="submit">Run Example</button>
                </form>
                <script>console.log({window.result})</script>
                <div>Example output : {window.result}</div>
            </div>
        </>
    );
}
