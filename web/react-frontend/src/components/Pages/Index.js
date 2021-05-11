import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";

import {Link, Route, BrowserRouter} from 'react-router-dom'
import ButtonDiv from "../Buttons/ButtonDiv";

export default function Index ({
    title
}) {
    return (
        <>  <BrowserRouter>
            <div className="container px-4 mx-auto pt-24 ">
                <div className="flex flex-wrap">
                    <div className="w-full px-4 flex-1"/>
                    <h1 className="text-5xl font-normal leading-normal mt-0 mb-2 text-lightBlue-600">{title}</h1>
                    <div className="w-full px-4 flex-1"/>
                </div>
            </div>
            <section className="mt-48 md:mt-40 pb-48 pt-32 relative">
                <div className="container px-0 mx-auto ">
                    <div className="flex flex-wrap">
                        <ButtonDiv
                            divText="Create your own CGG"
                            buttonText="Create CGG"
                            icon="fas fa-upload"
                            link="/page2"
                        />
                        <div className="w-full px-4 flex-1"/>
                        <ButtonDiv
                            divText="Load an existing example of CGG"
                            buttonText="Load CGG"
                            icon="fas fa-plus-circle"
                            link="/page2"
                        />
                    </div>
                </div>
            </section>

        </BrowserRouter>
        </>
    );
}
