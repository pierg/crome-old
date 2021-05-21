import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "./indexEnvironment";
import GridWorld from "./indexEnvironment";
import customsidebar from "../../_texts/custom/customsidebar";
import Sidebar from "../Sidebar/Sidebar";
import CustomPlayer from "./CustomPlayer";
import custommediaplayerteaminfo from "../../_texts/custom/custommediaplayerteaminfo";

export default class CreateEnvironment extends React.Component {

    constructor(props) {
        super(props);
        this.myRef = React.createRef();
        this.textInput = React.createRef();
        this.colorComponent = React.createRef();
        this.focusTextInput = this.focusTextInput.bind(this);

    }

    focusTextInput() {
        // Donne explicitement le focus au champ texte en utilisant l’API DOM native.
        // Remarque : nous utilisons `current` pour cibler le nœud DOM
        this.textInput.current.focus();
        this.buildGrid(this.myRef.current, this.textInput.current.value);
        this.colorComponent.current.hidden = false;
    }

    buildGrid(canvas, size) {
        // Update the document title using the browser API

        //let canvas= myCanvas;
        let map = [];

        for (let i = 0; i < size; i++) {
            map[i] = [];
            for (let j = 0; j < size; j++) {
                map[i].push(0);
            }
        }
        let world = new GridWorld(canvas, map[0].length, map.length, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true,
            onclick: function (node) {
                console.log("you clicked on node: " + node);
                if (node.x % 2 === 1) {
                    if (world.isBlocked(node.x, node.y)) {
                        world.setBackgroundColor(node.x, node.y, "white");
                        world.setBlocked(node.x, node.y, false);
                    }
                    else {
                        world.setBackgroundColor(node.x, node.y, "black");
                        world.setBlocked(node.x, node.y, true);
                    }
                }
                else {
                    if (world.isBlocked(node.x, node.y)) {
                        world.setBackgroundColor(node.x, node.y, "white");
                        world.setBlocked(node.x, node.y, false);
                    }
                    else if (node.y % 2 == 1) {
                        if (world.isBlocked(node.x, node.y)) {
                            world.setBackgroundColor(node.x, node.y, "black");
                            world.setBlocked(node.x, node.y, true);
                        }
                        else {
                            world.setBackgroundColor(node.x, node.y, "black");
                            world.setBlocked(node.x, node.y, true);
                        }
                    }
                    else {
                        const selectColor = document.getElementById("color");
                        const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>

                        const color = selectColor.options[choiceColor].text;
                        world.setBackgroundColor(node.x, node.y, color);
                        world.setBlocked(node.x, node.y, true);
                    }
                }
                world.draw();
            }
        });

        map.forEach(function (row, y) {
            row.forEach(function (cell, x) {
                if (cell) {
                    world.setBackgroundColor(x, y, 'black');
                    world.setBlocked(x, y, true);
                }
            })
        })

        world.draw();
    }
    render() {
        return (
            <>
                <Sidebar {...customsidebar} />
                <div className="relative md:ml-64 bg-blueGray-100">
                    <div>
                        <div>
                            <Sidebar {...customsidebar} />
                        </div>
                        <div>
                            <div> choose the size of the grid :
                                <input
                                    type="text"
                                    ref={this.textInput} />
                                <button onClick={this.focusTextInput}>Generate</button>
                            </div>
                            <canvas ref={this.myRef} id='canvas'/>
                            <select ref={this.colorComponent} hidden={true} id="color" name="color">
                                <option>blue</option>
                                <option>green</option>
                                <option>red</option>
                                <option>pink</option>
                                <option>purple</option>
                                <option>yellow</option>
                                <option>grey</option>
                                <option>white</option>
                            </select>
                        </div>
                    </div>
                </div>
            </>
        );
    }
}


