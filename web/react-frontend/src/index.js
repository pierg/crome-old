import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import {BrowserRouter} from "react-router-dom";
import {Route, Switch} from "react-router-dom";

// Components
import TabsF from "./components/Tabs/TabsF";
import Header from "./components/Pages/Header";
import FooterSmall from "./components/Footers/FooterSmall";
import WorldModeling from "./components/Pages/CreateCGG/WorldModeling";
import Index from "./components/Pages/Index";
import GoalModeling from "./components/Pages/GoalModeling";
import App from './App';
import CreateEnvironment from "./components/Pages/CreateCGG/CreateEnvironment";
import RunExample from "./components/Pages/RunExample";


//  Page create your own CGG

export const CreateCGG = () => {
    return (
        <React.StrictMode>
            <TabsF firstMenu={"Environment"} secondMenu={"World Modeling"} thirdMenu={"Goal Modeling"} fourthMenu={"Analysis"} fifthMenu={"Synthesis"}
                   firstPage={<></>}
                   secondPage={<WorldModeling firstCategory={"Actions"} secondCategory={"Sensors"} thirdCategory={"Context"}/>}
                   thirdPage={<></>}
                   fourthPage={<RunExample/>}
                   fifthPage={<></>}/>
        </React.StrictMode>
    );
};



ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <Header
                title={"Crome"}
                leftElement={"Other"}
                centerElement={"CGG"}
                rightElement={"About"}/>
            <Switch>
                <Route exact path="/">
                    <Index
                        title={"Contract-Based Goals Graph"}
                    />
                </Route>
                <Route path="/createCGG">
                    <CreateCGG/>
                </Route>
                <Route path="/goals">
                    <GoalModeling/>
                </Route>
            </Switch>
            <FooterSmall />
        </BrowserRouter>
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