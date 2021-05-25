import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "./indexEnvironment";
import GridWorld from "./indexEnvironment";
import customsidebar from "../../_texts/custom/customsidebar";
import CustomSidebar from "./CustomSidebar";

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
        this.buildGrid(this.myRef.current, this.textInput.current.value,this.map);
        this.colorComponent.current.hidden = false;
    }

    buildGrid(canvas, size) {
        // Update the document title using the browser API

        //let canvas= myCanvas;
        let map = [];
        if (map.length === 0) {
            for (let i = 0; i < size; i++) {
                map[i] = [];
                for (let j = 0; j < size; j++) {
                    map[i].push(0);
                }
            }
        }
        /*else {
            let map2 = map;
            let maxIdX = 0;
            let minIdX = map.length;
            let minIdY = map[0].length;
            let maxIdY = 0;
            for (let i = 0; i < map.length; i++) {
                for (let j = 0; j < map[0].length; j++) {
                    if (map[i][j] !== 0) {
                        if (minIdX > i) {
                            minIdX = i;
                        }
                        else if (maxIdX < i) {
                            maxIdX = i;
                        }
                        else if (minIdY > j) {
                            minIdY = j;
                        }
                        else if (maxIdY < j) {
                            maxIdY = j;
                        }
                    }
                }
            }
            maxIdX = map.length - maxIdX;
            maxIdY = map.length - maxIdY;

            if (minIdX < maxIdX) {
                let minX = minIdX
            }
            else {
                let minX =maxIdX;
            }
            if (minIdX < maxIdX) {
                let minX = minIdX
            }
            else {
                let minX =maxIdX;
            }

            map = [];
            for (let i = 0; i < size; i++) {
                map[i] = [];
                for (let j = 0; j < size; j++) {
                    if (map2[i  ])
                    map[i].push(0);
                }
            }


        }*/
        let world = new GridWorld(canvas, map[0].length, map.length, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true,
            onclick: function (node, start, end) {
                console.log("you clicked on node: " + node);
                if (node.x % 2 === 1 && node.y % 2 === 1) { // if the user click on a cell
                    if (end.length !== 0) { // when it's the second click, draw a square
                        let minX;
                        let maxX;
                        let maxY;
                        let minY;
                        if (start[0] < end[0]) {
                            minX = start[0];
                            maxX = end[0];
                        }
                        else {
                            minX = end[0];
                            maxX = start[0];
                        }
                        if (start[1] < end[1]) {
                            minY = start[1];
                            maxY = end[1];
                        }
                        else {
                            minY = end[1];
                            maxY = start[1];
                        }
                        for (let i = minX; i < maxX + 1; i += 1 ) {
                            for (let j = minY; j < maxY + 1; j += 1) {
                                const selectColor = document.getElementById("color");
                                const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>

                                const color = selectColor.options[choiceColor].text;
                                if (world.getBackgroundColor(i,j) !== color) {
                                    if (world.getBackgroundColor(i + 1, j) !== color) {
                                        world.setBackgroundColor(i + 1, j,"white");
                                    }
                                    if (world.getBackgroundColor(i - 1, j) !== color) {
                                        world.setBackgroundColor(i - 1, j,"white");
                                    }
                                    if (world.getBackgroundColor(i , j - 1) !== color) {
                                        world.setBackgroundColor(i, j - 1,"white");
                                    }
                                    if (world.getBackgroundColor(i , j + 1) !== color) {
                                        world.setBackgroundColor(i, j + 1,"white");
                                    }
                                }

                                world.setBackgroundColor(i, j, color);
                                world.setBlocked(i, j, true);
                                map[Math.trunc(i/2)][Math.trunc(j/2)] = color;
                            }
                        }
                    }
                    else { // when it's the first click, color the cell with a "light" color
                        const selectColor = document.getElementById("color");
                        const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>

                        const color = selectColor.options[choiceColor].text;
                        if (color === "red") {
                            world.setBackgroundColor(node.x, node.y, "#fd6969");
                            world.setBlocked(node.x, node.y, true);
                        }
                        else if(color === "purple") {
                            world.setBackgroundColor(node.x, node.y, "#e785ff");
                            world.setBlocked(node.x, node.y, true);
                        }
                        else {
                            const lightColor = "light" + color;
                            world.setBackgroundColor(node.x, node.y, lightColor);
                            world.setBlocked(node.x, node.y, true);
                        }
                    }
                }
                else {
                    if (world.isBlocked(node.x, node.y)) {
                        world.setBackgroundColor(node.x, node.y, "white");
                        world.setBlocked(node.x, node.y, false);
                    } else {
                        world.setBackgroundColor(node.x, node.y, "black");
                        world.setBlocked(node.x, node.y, true);
                    }
                }
                world.draw();
            }
        });

        map.forEach(function (row, y) {
            row.forEach(function (cell, x) {
                if (cell) {
                    world.setBackgroundColor(x, y, map[x][y]);
                    world.setBlocked(x, y, true);
                }
            })
        })

        world.draw();

    }
    render() {
        return (
            <>
                <CustomSidebar {...customsidebar} currentRoute={"#"+this.props.location} /> {/* TODO useLocation as in CustomDashboard */}
                <div className="relative md:ml-64 bg-blueGray-100">
                    <div>
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


