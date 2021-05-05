import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { StyleReset, Icon } from 'atomize';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {
  ThemeProvider,
  DefaultTheme,
  Div,
  Button,
  Text,
} from "atomize";
import CardStats from "./components/Cards/CardStats";
import IndexDropdown from "./components/Dropdowns/IndexDropdown";
import NotificationDropdown from "./components/Dropdowns/NotificationDropdown";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import { Provider as StyletronProvider, DebugEngine } from "styletron-react";
import { Client as Styletron } from "styletron-engine-atomic";

const debug =
  process.env.NODE_ENV === "production" ? void 0 : new DebugEngine();

// 1. Create a client engine instance
const engine = new Styletron();

ReactDOM.render(
  <React.StrictMode>
    <App />
    <NotificationDropdown />
      <StyletronProvider value={engine} debug={debug} debugAfterHydration>
      <Icon name="Add" size="20px"/>
      </StyletronProvider>
  </React.StrictMode>,
  document.getElementById('root')
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