import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import {
  Div,
  Text,
} from "atomize";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import { Provider as StyletronProvider, DebugEngine } from "styletron-react";
import { Client as Styletron } from "styletron-engine-atomic";

const debug =
  process.env.NODE_ENV === "production" ? void 0 : new DebugEngine();

// 1. Create a client engine instance
const engine = new Styletron();




export default function Header ({

}) {
    return (
        <>
            <StyletronProvider value={engine} debug={debug} debugAfterHydration>
            <Div bg={"#BCB3E2"} h={{ xs: 'auto', md: '10vh' }} d={"flex"} align={"center"} >
                <Div >logo</Div>
                <Div m={{l:"2%"}}><Text tag={"h2"} textSize="display2" textColor={"gray800"}>Crome</Text></Div>
                <Div m={{l:"35%"}}><Text tag={"h4"} textSize="subheader" textColor={"white"}>Other</Text></Div>
                <Div m={{l:"5%"}}><Text tag={"h4"} textSize="subheader" textColor={"white"}>CGG</Text></Div>
                <Div m={{l:"5%"}}><Text tag={"h4"} textSize="subheader" textColor={"white"}>About</Text></Div>
            </Div>
            </StyletronProvider>
        </>
    );
}
