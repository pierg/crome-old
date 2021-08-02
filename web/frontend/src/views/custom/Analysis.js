import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import * as cgg from "./cgg.json"
import goaleditinfo from "../../_texts/custom/goaleditinfo";
import cggsymbols from "../../_texts/custom/cggsymbols";
import {Modal} from "reactstrap";
import GoalModalView from "../../components/Custom/GoalModalView";
import CGG from "../../components/Crome/CGG";


export default class Analysis extends React.Component {

    state = {
        modalGoal: false,
        currentGoalIndex: 0,
    }

    setModalGoal = (bool) => {
        this.setState({
            modalGoal: bool
        })
    }

    setCurrentGoalIndex = (id) => {
        this.setState({
            currentGoalIndex: id
        })
    }

    render() {

        let that = this

        let nodesArray = []
        let edgesArray = []

        let goal

        function findGoalInCGGById(id) {
            for (const property in cgg.nodes) {
                if (cgg.nodes.hasOwnProperty(property)) {
                    if (cgg.nodes[property]["id"] === id[0]) return cgg.nodes[property]
                }
            }
            return {id: null}
        }

        function findGoalById(id) {
            for (let i=0; i<that.props.goals.length; i++) {
                if (that.props.goals[i].id === id) return that.props.goals[i]
            }
            return {name: "error"}
        }

        if (this.props.goals !== null) {
            cgg.nodes.forEach(function (node) {
                goal = findGoalById(node.id)
                nodesArray.push({
                    id: node.id,
                    group: node.hasOwnProperty("group") ? node.group : "input",
                    label: node.hasOwnProperty("name") ? node.name : goal.name
                })
            });
        }

        cgg.edges.forEach(function (node) {
            edgesArray.push({
                from: node.from,
                to: node.to,
                arrows: {to: {type: cggsymbols[node.type]}}
            })
        });

        const graph = {
            nodes: nodesArray,
            edges: edgesArray
        }

        const options = {
            layout: {
                hierarchical: true
            },
            edges: {
                color: "#000000",
                arrows: {
                    to: {
                        scaleFactor: 1
                    }
                }
            },
            nodes: {
                shape: "box"
            },
            groups: {
                input: {
                    color: {
                        border: "#00bb00",
                        background: "#ffffff",
                        highlight: {
                            border: "#88bb88",
                            background: "#ccccee"
                        }
                    }
                },
                new: {
                    color: {
                        border: "#00bb00",
                        background: "#00bb00",
                        highlight: {
                            border: "#88bb88",
                            background: "#bbffbb"
                        }
                    }
                },
                library: {
                    color: {
                        border: "#ffbb00",
                        background: "#ffffff",
                        highlight: {
                            border: "#ffbb88",
                            background: "#eeeecc"
                        }
                    }
                }
            },
            height: "1200px",
            autoResize: true,
            /*"physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -138,
                    "centralGravity": 0.02,
                    "springLength": 100
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based",
            }*/
        };



        function clickOnGoal(id) {
            const goal = findGoalInCGGById(id)
            if (!goal.hasOwnProperty("group")) {
                that.setModalGoal(true)
                that.setCurrentGoalIndex(id)
            }
        }
        const events = {
            doubleClick: function (event) {
                if (event.nodes.length !== 0) clickOnGoal(event.nodes)
            }
        };

        return (
            <>
                <CGG
                    active={this.props.active}
                    graph={graph}
                    options={options}
                    events={events}
                />
                <Modal
                    isOpen={this.state.modalGoal}
                    toggle={() => this.setModalGoal(false)}
                    className={"custom-modal-dialog sm:c-m-w-70 md:c-m-w-60 lg:c-m-w-50 xl:c-m-w-40"}>
                    {this.props.goals !== null && this.props.goals[this.state.currentGoalIndex] !== undefined && (
                        <GoalModalView
                        goal={this.props.goals[this.state.currentGoalIndex]}
                        close={() => this.setModalGoal(false)}
                        patterns={this.props.patterns}
                        {...goaleditinfo}/>
                    )}
                </Modal>
            </>
        );
    }
}