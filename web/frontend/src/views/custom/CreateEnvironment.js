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
        this.id = React.createRef();
        this.idBlock = React.createRef();
        this.divId = React.createRef();
    }

    focusTextInput() {
        this.textInput.current.focus();
        this.colorComponent.current.hidden = false;
        this.divId.current.hidden = false;
        this.buildGrid(this.myRef.current, this.textInput.current.value,this.id.current, this.idBlock.current,);
    }

    buildGrid(canvas, size, idInput, idBlock) {
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
            onclick: function (node, start, end ,startWall, endWall, previousStartColor, previousEndColor, previousColorWall) {
                const idToRemove = document.getElementById("idToRemove").value;
                if (idToRemove !== "") {
                    world.removeAttribute(idToRemove);
                    document.getElementById(idToRemove).innerHTML = "" ;
                    document.getElementById("idToRemove").value = "";
                    return false;

                }
                let id = idInput.value;
                const selectColor = document.getElementById("color");
                const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>
                const color = selectColor.options[choiceColor].text;
                if (node.x % 2 === 1 && node.y % 2 === 1) { // if the user click on a cell
                    if (end.length !== 0) { // when it's the second click, draw a square
                        if (id === "") { // when the user didn't input an id
                            console.log("you need to put an id");
                            world.setBackgroundColor(start[0],start[1], previousStartColor);
                            world.setBackgroundColor(startWall[0],startWall[1], previousColorWall);
                            world.draw();
                            return false;
                        }
                        else if (world.isAttribute(id, color) === true) { // when the user input an id that is already use
                            console.log("id already use");
                            world.setBackgroundColor(start[0],start[1], previousStartColor);
                            world.draw();
                            return ;
                        }
                        else {
                            let minX; // these variables allow to create only one loop for
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

                                    if (world.getBackgroundColor(i, j) !== color || world.getBackgroundColor(i, j) !== null) { //if the cell has already a color, color his neighbors in white
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

                                    world.setBackgroundColor(i, j, color); // color the cell with the color choose by the user
                                    world.setBlocked(i, j, true);
                                    world.setAttribute(i, j, "id", id); // the cell has a attribute id which have a value of the input of the user
                                    map[Math.trunc(i / 2)][Math.trunc(j / 2)] = color; // later : allow to save the environment when you generate with a different size
                                }
                            }
                            if (document.getElementById(id) === null || document.getElementById(id).innerHTML === "") {
                                idBlock.innerHTML += "<div id=" + id + ">Color : " + color + " id :" + id + "</div>";
                            }
                        }
                    } else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                        if (id === "") { // when the user didn't input an id
                            console.log("you need to put an id");
                            if (startWall.length !== 0) {
                                world.setBackgroundColor(startWall[0],startWall[1], previousColorWall);
                            }
                            world.draw();
                            return false;
                        } else {
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
                    }
                } else { // when you click on wall cell
                    if (endWall.length !== 0) { // when it's the second click
                        let min;
                        let max;
                        if (startWall[0] === endWall[0] && startWall[1] === endWall[1]) { // when you double-click on a wall
                            if (previousColorWall === "black") { // if the wall was black the background color will be white
                                world.setBackgroundColor(startWall[0], startWall[1], "white");
                                world.setBlocked(startWall[0], startWall[1], false);
                                world.draw();
                                return ;
                            } else if (previousColorWall === "white" || previousColorWall === null) { // if the wall was white the background color will be black
                                world.setBackgroundColor(startWall[0], startWall[1], "black");
                                world.setBlocked(startWall[0], startWall[1], true);
                                world.draw();
                                return ;
                            } else { // if the wall was neither black nor white, you can't change the background color
                                console.log("impossible");
                            }
                        } else if (startWall[0] === endWall[0]) {
                            if (startWall[0] % 2 === 1) { // when he clicks on a case that he can't choose
                                console.log("impossible");
                                world.setBackgroundColor(startWall[0], startWall[1], previousColorWall);
                            } else {
                                if (startWall[1] < endWall[1]) {
                                    min = startWall[1];
                                    max = endWall[1];
                                } else {
                                    min = endWall[1];
                                    max = startWall[1];
                                }
                                for (let i = min; i < max + 1; i += 1) {
                                    if (previousColorWall === "black") {
                                        world.setBackgroundColor(startWall[0], i, "white");
                                        world.setBlocked(startWall[0], i, false);
                                    } else if (world.isBlocked(startWall[0], i) && previousColorWall !== "black") { // when he clicks on a case that he can't choose
                                        console.log("Impossible");
                                    } else {
                                        world.setBackgroundColor(startWall[0], i, "black");
                                        world.setBlocked(startWall[0], i, true);
                                    }
                                }
                            }
                        } else if (startWall[1] === endWall[1]) {
                            if (startWall[1] % 2 === 1) { // when he clicks on a case that he can't choose
                                console.log("impossible");
                                world.setBackgroundColor(startWall[0], startWall[1], previousColorWall);
                            } else {
                                if (startWall[0] < endWall[0]) {
                                    min = startWall[0];
                                    max = endWall[0];
                                } else {
                                    min = endWall[0];
                                    max = startWall[0];
                                }
                                for (let i = min; i < max + 1; i += 1) {
                                    if (previousColorWall === "black") {
                                        world.setBackgroundColor(i, startWall[1], "white");
                                        world.setBlocked(i, startWall[1], false);
                                    } else if (world.isBlocked(i, startWall[1]) && previousColorWall !== "black") { // when he clicks on a case that he can't choose
                                        console.log("Impossible");
                                    } else {
                                        world.setBackgroundColor(i, startWall[1], "black");
                                        world.setBlocked(i, startWall[1], true);
                                    }
                                }
                            }
                        } else {
                            world.setBackgroundColor(startWall[0], startWall[1], "white");
                        }
                    } else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                        if (world.getBackgroundColor(node.x, node.y) === "white" || world.getBackgroundColor(node.x, node.y) === "black" || world.getBackgroundColor(node.x, node.y) === null) {
                            world.setBackgroundColor(node.x, node.y, "lightgray");
                        } else { // when he clicks on a case that he can't choose
                            console.log("Impossible");
                        }
                    }
                }
                world.draw();
            }
        });
        world.clearAttributeTable();
        idBlock.innerHTML = "";
        map.forEach(function (row, y) {
            row.forEach(function (cell, x) {
                if (cell) {
                    world.setBackgroundColor(x, y, "black");
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
                                ref={this.textInput}
                            />
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
                        <input ref={this.id}/>
                        <div ref={this.divId} hidden={true}> choose an id to remove :
                            <input id={"idToRemove"}
                                   type="text"/>
                        </div>
                        <div ref={this.idBlock}/>
                    </div>
                </div>
            </>
        );
    }
}


