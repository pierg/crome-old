import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import {BrowserRouter} from "react-router-dom";
import {Route, Switch} from "react-router";

// Components
import TabsF from "./components/Tabs/TabsF";
import Header from "./components/Pages/Header";
import FooterSmall from "./components/Footers/FooterSmall";
import WorldModeling from "./components/Pages/WorldModeling";
import Index from "./components/Pages/Index";
import App from './App';


//  Page create your own CGG

export const CreateCGG = () => {
    return (

        <React.StrictMode>
            <TabsF firstMenu={"Environment"} secondMenu={"World Modeling"} thirdMenu={"Goal Modeling"} fourthMenu={"Analysis"} fifthMenu={"Synthesis"}
                   firstPage={<></>}
                   secondPage={<WorldModeling firstCategory={"Actions"} secondCategory={"Sensors"} thirdCategory={"Context"}/>}
                   thirdPage={<></>}
                   fourthPage={<></>}
                   fifthPage={<></>}/>
        </React.StrictMode>
    );
};



ReactDOM.render(
    <React.StrictMode>
        <Header
            title={"Crome"}
            leftElement={"Other"}
            centerElement={"CGG"}
            rightElement={"About"}/>

        <BrowserRouter>
            <Switch>
                <Route exact path="/">
                    <Index
                        title={"Contract-Based Goals Graph"}
                    />
                </Route>
                <Route path="/createCGG">
                    <CreateCGG/>
                </Route>
            </Switch>
        </BrowserRouter>
        <FooterSmall />
    </React.StrictMode>,
    document.getElementById('root')
);

export default function Main() {
    return (
        <>
            <App />

        </>
    );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();