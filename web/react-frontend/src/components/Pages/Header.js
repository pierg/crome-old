import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import {
  Div,
  Text,
  Row,
  Col
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
    title,
    leftElement,
    centerElement,
    rightElement
}) {
    return (
        <>
            <StyletronProvider value={engine} debug={debug} debugAfterHydration>
                <Row bg={"#8dc9f0"} textAlign="center" align="center" fontFamily="Roboto" m={{ l: '0', r: '0' }}>
                    <Col size={{ xs: 12, lg: 1 }}>
                        <Div p="1rem">
                            Logo
                        </Div>
                    </Col>
                    <Col size={{ xs: 12, lg: 1 }}>
                        <Div p="1rem" textAlign={{ xs: "center", lg: "left" }} textColor={"white"}>
                            <Text tag={"h2"} textSize="display2" textColor={"gray300"}>{title}</Text>
                        </Div>
                    </Col>
                    <Col size={{ xs: 12, lg: 8 }}>
                        <Div p="1rem">
                            <Row textColor={"white"} textWeight="200" textSize="heading">
                                <Col size={{ xs: 12, lg: 3 }}>
                                    <Div p="1rem"/>
                                </Col>
                                <Col size={{ xs: 12, lg: 2 }}>
                                    <Div p="1rem">
                                        <Text>{leftElement}</Text>
                                    </Div>
                                </Col>
                                <Col size={{ xs: 12, lg: 2 }}>
                                    <Div p="1rem">
                                        <Text>{centerElement}</Text>
                                    </Div>
                                </Col>
                                <Col size={{ xs: 12, lg: 2 }}>
                                    <Div p="1rem">
                                        <Text>{rightElement}</Text>
                                    </Div>
                                </Col>
                                <Col size={{ xs: 12, lg: 3 }}>
                                    <Div p="1rem"/>
                                </Col>
                            </Row>
                        </Div>
                    </Col>
                    <Col size={{ xs: 12, lg: 2 }}>
                        <Div p="1rem"/>
                    </Col>
                </Row>
            </StyletronProvider>
        </>
    );
}
/*
<Div bg={"#8dc9f0"} h={{ xs: 'auto', md: '15vh' }} d={"flex"} align={"center"} >
                <Div >logo</Div>
                <Div m={{l:"2%"}}><Text tag={"h2"} textSize="display2" textColor={"gray800"}>Crome</Text></Div>
                <Div m={{l:"35%"}}><Text tag={"h4"} textSize="subheader" textColor={"white"}>Other</Text></Div>
                <Div m={{l:"5%"}}><Text tag={"h4"} textSize="subheader" textColor={"white"}>CGG</Text></Div>
                <Div m={{l:"5%"}}><Text tag={"h4"} textSize="subheader" textColor={"white"}>About</Text></Div>
            </Div>
 */