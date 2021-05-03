import logo from './logo.svg';
import './App.css';
import {
  ThemeProvider,
  DefaultTheme,
  StyleReset,
  Div,
  Button,
  Text,
  Icon
} from "atomize";
import ReactDOM from "react-dom";
import React from "react";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <form action="/example/" method="post">
          <select name="exampleButtons">
            <option>0_modeling_goals</option>
            <option>1_analysis_build_cgg</option>
            <option>2_synthesis_realize_controllers</option>
            <option>3_simulation_orchestrate</option>
          </select>
          <button name="submitExample" type="submit">Run Example</button>
        </form>
        <div>Example output : {window.result}</div>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>My Token = {window.token}</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);

export default App;
