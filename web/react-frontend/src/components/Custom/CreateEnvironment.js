import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "./indexEnvironment";
import GridWorld from "./indexEnvironment";
import customsidebar from "../../_texts/admin/sidebar/customsidebar";
import Sidebar from "../Sidebar/Sidebar";
import CustomPlayer from "./CustomPlayer";
import custommediaplayerteaminfo from "../../_texts/e-commerce/mediaplayers/custommediaplayerteaminfo";

export default class CreateEnvironment extends React.Component {

    constructor(props) {
        super(props);
        this.myRef = React.createRef();

    }

    componentDidMount() {
        // we can use this.inputRef.current to access DOM element
        this.buildGrid(this.myRef.current);
    }

    buildGrid(canvas) {
        // Update the document title using the browser API

        //let canvas= myCanvas;

        let map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ];
        let world = new GridWorld(canvas, map[0].length, map.length, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true,
            onclick: function (node) {
                console.log("you clicked on node: " + node);
                if (node.x % 2 === 1) {
                    world.setBackgroundColor(node.x, node.y, "black");
                    world.setBlocked(node.x, node.y, true);
                    console.log(world.nodes[(node.y * world.width) + node.x]["id"]);
                }
                else {
                    const selectColor = document.getElementById("color");
                    const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>

                    const color = selectColor.options[choiceColor].text;

                    const selectId = document.getElementById("id");
                    const choiceId = selectId.selectedIndex;  // Take the index of the chosen <option>
                    const id = selectId.options[choiceId].text;
                    world.setBackgroundColor(node.x, node.y, color);
                    world.setBlocked(node.x, node.y, true);
                    world.setAttribute(node.x, node.y, "id", id);
                    console.log(world.nodes[(node.y * world.width) + node.x]["id"]);
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
                            <canvas ref={this.myRef} id='canvas' width='920' height='640'/>
                            <select id="color" name="color">
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


