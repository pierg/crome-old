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
                /*
                start is an array where the coordinates of the first click are stored if it is a cell
                end is an array where the coordinates of the second click are stored if it is a cell
                startWall is an array where the coordinates of the first click are stored if it is a wall
                endWall is an array where the coordinates of the first click are stored if it is a wall
                previousStartColor is a variable where the colour before the first click is stored if it is a cell
                previousEndColor is a variable where the colour before the second click is stored if it is a cell
                previousColorWall is a variable where the colour before the first click is stored if it is a wall
                */
                const idToRemove = document.getElementById("idToRemove").value;
                document.getElementById("comment").innerHTML = "";
                if (idToRemove !== "") {
                    world.removeAttribute(idToRemove);
                    document.getElementById(idToRemove).innerHTML = "" ;
                    document.getElementById("idToRemove").value = "";
                    return false; // allow to reset start, end, startWall, endWall

                }
                let id = idInput.value;
                const selectColor = document.getElementById("color");
                const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>
                const color = selectColor.options[choiceColor].text;
                if (node.x % 2 === 1 && node.y % 2 === 1) { // if the user click on a cell
                    if (end.length !== 0) { // when it's the second click, draw a square
                        if (id === "") { // when the user didn't input an id
                            document.getElementById("comment").innerHTML = "you need to put an id";
                            world.setBackgroundColor(start[0],start[1], previousStartColor);
                            world.setBackgroundColor(startWall[0],startWall[1], previousColorWall);
                            world.draw();
                            return false; // allow to reset start, end, startWall, endWall
                        }
                        else if (world.isAttribute(id, color) === true) { // when the user input an id that is already use
                            document.getElementById("comment").innerHTML = "id or color already use";
                            world.setBackgroundColor(start[0],start[1], previousStartColor);
                            world.draw();
                            return ;
                        }
                        else {
                            let minX = world.min(start[0],end[0])[0]; // these variables allow to create only one loop for
                            let maxX = world.min(start[0],end[0])[1];
                            let maxY = world.min(start[1],end[1])[1];
                            let minY = world.min(start[1],end[1])[0];
                            for (let i = minX; i < maxX + 1; i += 1) {
                                for (let j = minY; j < maxY + 1; j += 1) {

                                    world.checkNeighbour(i, j, color); //if the cell has already a color, color his neighbors in white except if there is a wall
                                    world.setColorIdBlocked(i, j, color, true, id);
                                    map[Math.trunc(i / 2)][Math.trunc(j / 2)] = color; // later : allow to save the environment when you generate with a different size
                                }
                            }
                            if (document.getElementById(id) === null || document.getElementById(id).innerHTML === "") {
                                idBlock.innerHTML += "<div id=" + id + ">Color : " + color + " id :" + id + "</div>";
                            }
                        }
                    } else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                        if (id === "") { // when the user didn't input an id
                            document.getElementById("comment").innerHTML = "you need to put an id";
                            if (startWall.length !== 0) {
                                world.setBackgroundColor(startWall[0],startWall[1], previousColorWall);
                            }
                            world.draw();
                            return false; // allow to reset start, end, startWall, endWall
                        } else {
                            if (color === "red") {
                                world.setBackgroundColor(node.x, node.y, "#fd6969");
                            } else if (color === "purple") {
                                world.setBackgroundColor(node.x, node.y, "#e785ff");
                            } else {
                                const lightColor = "light" + color;
                                world.setBackgroundColor(node.x, node.y, lightColor);
                            }
                        }
                    }
                } else { // when you click on wall cell
                    if (endWall.length !== 0) { // when it's the second click
                        let min;
                        let max;
                        if (startWall[0] === endWall[0] && startWall[1] === endWall[1]) { // when you double-click on a wall
                            if (previousColorWall === "black") { // if the wall was black the background color will be white
                                world.setColorIdBlocked(startWall[0], startWall[1], "white", false, null);
                                world.draw();
                                return ;
                            } else if (previousColorWall === "white" || previousColorWall === null) { // if the wall was white the background color will be black
                                world.setColorIdBlocked(startWall[0], startWall[1], "black", true, null);
                                world.draw();
                                return;
                            } else { // if the wall was neither black nor white, you can't change the background color
                                document.getElementById("comment").innerHTML = "you can't change the color of this wall";
                                return false;
                            }
                        } else if (startWall[0] === endWall[0]) {
                            if (startWall[0] % 2 === 1) { // when he clicks on a case that he can't choose
                                document.getElementById("comment").innerHTML = "you have to select a row/column to change the colour of the walls";
                                world.setBackgroundColor(startWall[0], startWall[1], previousColorWall);
                            } else {
                                min = world.min(startWall[1],endWall[1])[0];
                                max = world.min(startWall[1],endWall[1])[1];
                                for (let i = min; i < max + 1; i += 1) {
                                    if (world.isBlocked(startWall[0], i) && previousColorWall !== "black") {// when he clicks on a case that he can't choose
                                        document.getElementById("comment").innerHTML = "you cannot select these, there are wall inside a block";
                                        world.setBackgroundColor(startWall[0], startWall[1], previousColorWall);
                                        return false;
                                    }
                                }
                                for (let i = min; i < max +1; i+= 1) {
                                    if (previousColorWall === "black") {
                                        world.setColorIdBlocked(startWall[0], i, "white", false, null);
                                    } else {
                                        world.setColorIdBlocked(startWall[0], i, "black", true, null);
                                    }
                                }
                            }
                        } else if (startWall[1] === endWall[1]) {
                            if (startWall[1] % 2 === 1) { // when he clicks on a case that he can't choose
                                document.getElementById("comment").innerHTML = "you have to select a row/column to change the colour of the walls";
                                world.setBackgroundColor(startWall[0], startWall[1], previousColorWall);
                                return false;
                            } else {
                                min = world.min(startWall[0],endWall[0])[0];
                                max = world.min(startWall[0],endWall[0])[1];

                                for (let i = min; i < max + 1; i += 1) {
                                     if (world.isBlocked(i, startWall[1]) && previousColorWall !== "black") { // when he clicks on a case that he can't choose
                                        document.getElementById("comment").innerHTML = "you cannot select these, there are wall inside a block";
                                        world.setBackgroundColor(startWall[0], startWall[1], previousColorWall);
                                        return false;
                                    }
                                }
                                for (let i = min; i < max +1; i+= 1) {
                                    if (previousColorWall === "black") {
                                        world.setColorIdBlocked(i, startWall[1], "white", false, null);
                                    } else {
                                        world.setColorIdBlocked(i, startWall[1], "black", true, null);
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
                            document.getElementById("comment").innerHTML = "you cannot select a wall within a block";
                            return false;
                        }
                    }
                }
                world.draw();
            }
        });
        world.clearAttributeTable();
        idBlock.innerHTML = "";
        document.getElementById("comment").innerHTML = "";

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
                        <input id={"id"} ref={this.id}/>
                        <div ref={this.divId} hidden={true}> choose an id to remove :
                            <input id={"idToRemove"}
                                   type="text"/>
                        </div>
                        <div id={"comment"}/>
                        <div ref={this.idBlock}/>
                    </div>
                </div>
            </>
        );
    }
}


