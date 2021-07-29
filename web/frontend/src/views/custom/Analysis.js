import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import Graph from "react-graph-vis";


export default class Analysis extends React.Component {

    state = {
        network: null,
        ready: false
    }

    componentDidUpdate(prevProps, prevState, snapshot) {

    }
    componentDidMount() {

    }

    setReady = (bool) => {
        this.setState({
            ready: bool
        })
    }

    render() {

        const graph = {
            nodes: [
                { id: 1, group: "new", label: "Node 1" },
                { id: 2, group: "input", label: "Node 2" },
                { id: 3, group: "input", label: "Node 3" },
                { id: 4, group: "input", label: "Node 4" },
                { id: 5, group: "new", label: "Node 5" },
                { id: 6, group: "input", label: "Node 6" },
                { id: 7, group: "new", label: "Node 7" },
                { id: 8, group: "input", label: "Node 8" },
                { id: 9, group: "input", label: "Node 9" },
                { id: 10, group: "input", label: "Node 10" },
                { id: 11, group: "library", label: "Node 11" },
                { id: 12, group: "library", label: "Node 12" },
                { id: 13, group: "library", label: "Node 13" },
                { id: 14, group: "new", label: "Node 14" },
                { id: 15, group: "library", label: "Node 15" },
                { id: 16, group: "library", label: "Node 16" },
            ],
            edges: [
                { from: 2, to: 1, arrows: {to: {type: "circle" }} },
                { from: 3, to: 1, arrows: {to: {type: "circle" }} },
                { from: 4, to: 1, arrows: {to: {type: "circle" }} },
                { from: 5, to: 2, arrows: {to: {type: "vee" }} },
                { from: 6, to: 3, arrows: {to: {type: "vee" }} },
                { from: 7, to: 4, arrows: {to: {type: "vee" }} },
                { from: 8, to: 5, arrows: {to: {type: "diamond" }} },
                { from: 9, to: 5, arrows: {to: {type: "diamond" }} },
                { from: 10, to: 5, arrows: {to: {type: "diamond" }} },
                { from: 11, to: 6, arrows: {to: {type: "vee" }} },
                { from: 12, to: 7, arrows: {to: {type: "diamond" }} },
                { from: 13, to: 7, arrows: {to: {type: "diamond" }} },
                { from: 14, to: 13, arrows: {to: {type: "vee" }} },
                { from: 15, to: 14, arrows: {to: {type: "diamond" }} },
                { from: 16, to: 14, arrows: {to: {type: "diamond" }} },

            ]
        };

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
            select: function(event) {
                const {nodes, edges} = event;
                console.log(nodes+edges)
            }
        };

        return (
            <div className="bg-lightBlue-500 bg-opacity-25">
                {this.state.ready && (<Graph
                    graph={graph}
                    options={options}
                    events={events}
                    getNetwork={network => {
                        this.setState({
                            network: network
                        })
                        //  if you want access to vis.js network api you can set the state in a parent component using this property
                    }}
                />)}
                {this.props.active && (<DelayActivation callBack={this.setReady}/>)}
            </div>
        );
    }
}

class DelayActivation extends React.Component {
    componentDidMount() {
        let callBack = this.props.callBack
        setTimeout(function(){callBack(true)},1000)
    }
    render() {
        return null;
    }
}