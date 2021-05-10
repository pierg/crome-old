import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { StyleReset, Icon } from 'atomize';
import App from './App';
import reportWebVitals from './reportWebVitals';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";


import {
  ThemeProvider,
  DefaultTheme,
  Div,
  Button,
  Text,
} from "atomize";
import CardStats from "./components/Cards/CardStats";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import { Provider as StyletronProvider, DebugEngine } from "styletron-react";
import { Client as Styletron } from "styletron-engine-atomic";
import TableDropdownF from "./components/Dropdowns/TableDropdownF";
import HeaderStats from "./components/Headers/HeaderStats";
import TabsF from "./components/Tabs/TabsF";
import Header from "./components/Pages/Header";
import Index from "./components/Pages";
import Footer from "./components/Footers/Footer";
import FooterSmall from "./components/Footers/FooterSmall";
import WorldModeling from "./components/Pages/WorldModeling";



const debug =
  process.env.NODE_ENV === "production" ? void 0 : new DebugEngine();

// 1. Create a client engine instance
const engine = new Styletron();

ReactDOM.render(
  <React.StrictMode>
        <StyletronProvider value={engine} debug={debug} debugAfterHydration>
        </StyletronProvider>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

ReactDOM.render(
    <React.StrictMode>
            <Header/>
            <Index />
            <FooterSmall />
        <TabsF firstMenu={"Environment"} secondMenu={"World Modeling"} thirdMenu={"Goal Modeling"} fourthMenu={"Analysis"} fifthMenu={"Synthesis"} firstPage={<></>} secondPage={<WorldModeling />} thirdPage={<></>} fourthPage={<></>} fifthPage={<></>}/>
    </React.StrictMode>,
    document.getElementById('index')
);


export default function Main() {
  return (
    <>
      <StyleReset />
      <App />

    </>
  );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();