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
        <Icon name="Add" color="white" size="20px" />
        <form action="/example/" method="post">
          <button name="forwardBtn" type="submit">Run Example 1</button>
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
