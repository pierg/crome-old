import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import goaleditinfo from "../../_texts/custom/goaleditinfo";
import cgginfo from "../../_texts/custom/cgginfo";
import {Modal} from "reactstrap";
import GoalModalView from "../../components/Custom/GoalModalView";
import CGG from "../../components/Crome/CGG";
import GetCGG from "../../components/Custom/Examples/GetCGG";
import BuildCGG from "../../components/Custom/BuildCGG";
import SocketBuildCGG from "../../components/Custom/Examples/SocketBuildCGG";
import IndexCGG from "../../components/Custom/IndexCGG";


export default class Analysis extends React.Component {

    state = {
        modalGoal: false,
        currentGoalIndex: 0,
        cgg: null,
        operator: null,
        selectedGoals: [],
        selectedLibrary: null,
        library: null,
        triggerOperation: false,
        triggerCGG: false
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

    callCGG = (mode) => {
        if (mode === "auto") {
            this.setState({
                triggerCGG: true
            })
        }
    }

    setCGG = (cgg) => {
        if (cgg !== null) {
            this.setState({
                cgg: JSON.parse(cgg),
                triggerCGG: false
            })
        }
    }

    setOperator = (operator) => {
        this.setState({
            operator: operator
        })
    }

    setSelectedGoals = (selectedGoals) => {
        this.setState({
            selectedGoals: selectedGoals
        })
    }

    setLibrary = (library) => {
        this.setState({
            selectedLibrary: library
        })
    }

    applyOperator = () => {
        this.setTriggerOperation(true)
    }

    setTriggerOperation = (bool) => {
        if (!bool) {
            this.setTriggerCGG(true)
        }
        this.setState({
            triggerOperation: bool
        })
    }

    setTriggerCGG = (bool) => {
        this.setState({
            triggerCGG: bool
        })
    }

    render() {

        let that = this

        function findGoalInCGGById(id) {
            for (const property in that.state.cgg.nodes) {
                if (that.state.cgg.nodes.hasOwnProperty(property)) {
                    if (that.state.cgg.nodes[property]["id"] === id[0]) return that.state.cgg.nodes[property]
                }
            }
            return {id: null}
        }

        function findGoalById(id) {
            if (that.props.goals !== null) {
                for (let i = 0; i < that.props.goals.length; i++) {
                    if (that.props.goals[i].id === id) return that.props.goals[i]
                }
            }
            if (that.state.cgg !== null) {
                for (let i = 0; i < that.state.cgg.nodes.length; i++) {
                    if (that.state.cgg.nodes[i].id === id) return that.state.cgg.nodes[i]
                }
            }
            return {name: "error"}
        }

        function clickOnGoal(id) {
            const goal = findGoalInCGGById(id)
            if (!goal.hasOwnProperty("group")) {
                that.setModalGoal(true)
                that.setCurrentGoalIndex(id)
            }
        }

        let nodesArray = []
        let edgesArray = []


        /* IF JSON IS RECEIVED */
        if (this.state.cgg !== null) {
            /* FILL CGG NODES FROM RECEIVED JSON */
            if (this.props.goals !== null) {
                let goal
                this.state.cgg.nodes.forEach(function (node) {
                    goal = findGoalById(node.id)
                    nodesArray.push({
                        id: node.id,
                        group: node.hasOwnProperty("group") ? node.group : "input",
                        label: node.hasOwnProperty("name") ? node.name : goal.name
                    })
                });
            }

            /* FILL CGG EDGES FROM RECEIVED JSON */
            this.state.cgg.edges.forEach(function (node) {
                edgesArray.push({
                    from: node.from,
                    to: node.to,
                    arrows: {to: {type: cgginfo.symbols[node.type]}}
                })
            });
        }


        /* DEFINE CGG PARAMETERS PASSED TO CGG COMPONENT */
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

        const events = {
            doubleClick: function (event) {
                if (event.nodes.length !== 0) clickOnGoal(event.nodes)
            }
        };

        return (
            <>
                <GetCGG updateCGG={this.setCGG} session={this.props.id} trigger={this.state.triggerCGG} setTrigger={this.setTriggerCGG}/>
                <SocketBuildCGG
                    session={this.props.id}
                    operator={this.state.operator}
                    goals={this.state.selectedGoals}
                    library={this.state.selectedLibrary}
                    trigger={this.state.triggerOperation}
                    setTrigger={this.setTriggerOperation}
                />
                {this.state.cgg === null && (<IndexCGG callCGG={this.callCGG}/>)}
                <BuildCGG
                    infos={cgginfo}
                    cgg={this.state.cgg}
                    goals={this.props.goals}
                    findGoalById={findGoalById}
                    selectedOperator={this.state.operator}
                    setOperator={this.setOperator}
                    selectedGoals={this.state.selectedGoals}
                    updateSelectedGoals={this.setSelectedGoals}
                    selectedLibrary={this.state.selectedLibrary}
                    setLibrary={this.setLibrary}
                    applyOperator={this.applyOperator}/>
                {this.state.cgg !== null && (<>
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
                    </Modal></>)}
            </>
        );
    }
}