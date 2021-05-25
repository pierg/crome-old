import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../components/Crome/IndexEnvironment";
import GridWorld from "../../components/Crome/IndexEnvironment";

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
            onclick: function (node, start, end ,startWall, endWall) {
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
                        } else {
                            minX = end[0];
                            maxX = start[0];
                        }
                        if (start[1] < end[1]) {
                            minY = start[1];
                            maxY = end[1];
                        } else {
                            minY = end[1];
                            maxY = start[1];
                        }
                        for (let i = minX; i < maxX + 1; i += 1) {
                            for (let j = minY; j < maxY + 1; j += 1) {
                                const selectColor = document.getElementById("color");
                                const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>

                                const color = selectColor.options[choiceColor].text;
                                if (world.getBackgroundColor(i, j) !== color || world.getBackgroundColor(i, j) !== null) {
                                    if (world.getBackgroundColor(i + 1, j) !== color) {
                                        world.setBackgroundColor(i + 1, j, "white");
                                        world.setBlocked(i + 1, j, false);
                                    }
                                    if (world.getBackgroundColor(i - 1, j) !== color) {
                                        world.setBackgroundColor(i - 1, j, "white");
                                        world.setBlocked(i - 1, j, false);
                                    }
                                    if (world.getBackgroundColor(i, j - 1) !== color) {
                                        world.setBackgroundColor(i, j - 1, "white");
                                        world.setBlocked(i, j - 1, false);
                                    }
                                    if (world.getBackgroundColor(i, j + 1) !== color) {
                                        world.setBackgroundColor(i, j + 1, "white");
                                        world.setBlocked(i, j + 1, false);
                                    }
                                }

                                world.setBackgroundColor(i, j, color);
                                world.setBlocked(i, j, true);
                                map[Math.trunc(i / 2)][Math.trunc(j / 2)] = color;
                            }
                        }
                    } else { // when it's the first click, color the cell with a "light" color
                        const selectColor = document.getElementById("color");
                        const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>

                        const color = selectColor.options[choiceColor].text;
                        if (color === "red") {
                            world.setBackgroundColor(node.x, node.y, "#fd6969");
                            world.setBlocked(node.x, node.y, true);
                        } else if (color === "purple") {
                            world.setBackgroundColor(node.x, node.y, "#e785ff");
                            world.setBlocked(node.x, node.y, true);
                        } else {
                            const lightColor = "light" + color;
                            world.setBackgroundColor(node.x, node.y, lightColor);
                            world.setBlocked(node.x, node.y, true);
                        }
                    }
                } else { // when you click on wall cell
                    if (endWall.length !== 0) { // when it's the second click
                        let min;
                        let max;
                        if (startWall[0] === endWall[0]) {
                            if (startWall[1] < endWall[1]) {
                                min = startWall[1];
                                max = endWall[1];
                            } else {
                                min = endWall[1];
                                max = startWall[1];
                            }
                            for (let i = min; i < max + 1; i += 1) {
                                if (world.isBlocked(startWall[0], i) && world.getBackgroundColor(startWall[0], i) === "black") {
                                    world.setBackgroundColor(startWall[0], i, "white");
                                    world.setBlocked(startWall[0], i, false);
                                }
                                else if (world.isBlocked(startWall[0], i) && world.getBackgroundColor(startWall[0], i) !== "black") {
                                    console.log("Impossible");
                                }
                                else {
                                    world.setBackgroundColor(startWall[0], i, "black");
                                    world.setBlocked(startWall[0], i, true);
                                }
                            }
                        } else if (startWall[1] === endWall[1]) {
                            if (startWall[0] < endWall[0]) {
                                min = startWall[0];
                                max = endWall[0];
                            } else {
                                min = endWall[0];
                                max = startWall[0];
                            }
                            for (let i = min; i < max + 1; i += 1) {
                                if (world.isBlocked(i, startWall[1]) && world.getBackgroundColor(i, startWall[1]) === "black") {
                                    world.setBackgroundColor(i, startWall[1], "white");
                                    world.setBlocked(i, startWall[1], false);
                                }
                                else if (world.isBlocked(i, startWall[1]) && world.getBackgroundColor(i, startWall[1]) !== "black") {
                                    console.log("Impossible");
                                }
                                else {
                                    world.setBackgroundColor(i, startWall[1], "black");
                                    world.setBlocked(i, startWall[1], true);
                                }
                            }
                        }
                        else {
                            world.setBackgroundColor(startWall[0], startWall[1], "white");
                        }
                    } else {
                        if (world.getBackgroundColor(node.x, node.y) === "white" || world.getBackgroundColor(node.x, node.y) === "black" || world.getBackgroundColor(node.x, node.y) === null) {
                            world.setBackgroundColor(node.x, node.y, "lightgray");
                        }
                        else {
                            console.log("Impossible");
                        }

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
            </>
        );
    }
}


