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
import { Provider as StyletronProvider, DebugEngine } from "styletron-react";
import { Client as Styletron } from "styletron-engine-atomic";

const debug =
  process.env.NODE_ENV === "production" ? void 0 : new DebugEngine();

// 1. Create a client engine instance
const engine = new Styletron();

function App() {
  return (
      <> </>
  /*    <StyletronProvider value={engine} debug={debug} debugAfterHydration>
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
      </header>
    </div>
      </StyletronProvider> */
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);

export default App;
