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
        this.generateGridworld = this.generateGridworld.bind(this);
        this.id = React.createRef();
        this.idBlock = React.createRef();
        this.divId = React.createRef();
        this.map = [];
    }

    generateGridworld() {
        const context = this.myRef.current.getContext('2d');
        context.clearRect(0, 0, this.myRef.current.width, this.myRef.current.height);
        this.textInput.current.focus();
        this.colorComponent.current.hidden = false;
        this.divId.current.hidden = false;
        this.buildGrid(this.myRef.current, this.textInput.current.value,this.id.current, this.idBlock.current, this.map);
    }

    buildMap(map, size) {
        for (let i = 0; i < size * 2 + 1; i++) {
            map[i] = [];
            for (let j = 0; j < size * 2 + 1; j++) {
                map[i].push(0);
            }
        }
    }
    inf(x, i, color, bool) {
        if (bool) {
            if (x[0] === i && color !== "black") {
                x[0] = i;
                x[1] = color;
            } else if (x[0] === i && color === "black") {}
            else {
                x[0] = i;
                x[1] = color;
            }
        }
        return x;
    }


    buildGrid(canvas, size, idInput, idBlock, map) {
        if (map.length === 0) {
            this.buildMap(map, size);
        }
        else {
            let map2 = map;
            let maxIdX = [0,null];
            let minIdX = [map.length, null];
            let minIdY = [map[0].length, null];
            let maxIdY = [0, null];
            for (let i = 0; i < map.length; i++) {
                for (let j = 0; j < map[0].length; j++) {
                    if (map[i][j][0] !== "white") {
                        minIdX = this.inf(minIdX, i, map[i][j][0], minIdX[0] >= i);
                        minIdY = this.inf(minIdY, j, map[i][j][0], minIdY[0] >= j);
                        maxIdX = this.inf(maxIdX, i, map[i][j][0], maxIdX[0] <= i);
                        maxIdY = this.inf(maxIdY, j, map[i][j][0], maxIdY[0] <= j);
                    }
                }
            }
            console.log("minIdX :" + minIdX);
            console.log("maxIdX :" + maxIdX);
            console.log("minIdY :" + minIdY);
            console.log("maxIdY :" + maxIdY);
            let oldSizeX = maxIdX[0] - minIdX[0] + 1;
            let oldSizeY = maxIdY[0] - minIdY[0] + 1;
            let isInX = (size * 2 + 1) - oldSizeX;
            let isInY = (size * 2 + 1) - oldSizeY;

            if (isInX < 0 || isInY < 0) {
                console.log("test");
            }
            else {

                let leftBorderX = Math.trunc(isInX / 2);
                let topBorderY = Math.trunc(isInY / 2);
                console.log("X : " + leftBorderX + "color : " + minIdX[1]);
                console.log("y :" + topBorderY + "color : " + minIdY[1]);
                if (leftBorderX % 2 === 1 && minIdX[1] === "black") {
                    console.log("test1");
                    leftBorderX++;
                }
                else if (leftBorderX % 2 === 0 && minIdX[1] !== "black") {
                    console.log("test2");
                    leftBorderX++;
                }
                if (topBorderY % 2 === 1 && minIdY[1] === "black") {
                    console.log("test3");
                    topBorderY++;
                }
                else if (topBorderY % 2 === 0 && minIdY[1] !== "black") {
                    console.log("test4");
                    topBorderY++;
                }
                map = [];

                this.buildMap(map, size);

                for (let i = leftBorderX; i < leftBorderX + oldSizeX; i++) {
                    for (let j = topBorderY; j < topBorderY + oldSizeY; j++) {
                        map[i][j] = map2[minIdX[0] + i - leftBorderX][minIdY[0] + j - topBorderY];
                    }
                }
            }

        }
        let world = new GridWorld(canvas, size, size, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true,
            onclick: function (node, start, end ,startWall, endWall, previousStartColor, previousColorWall) {
                /*
                start is an array where the coordinates of the first click are stored if it is a cell
                end is an array where the coordinates of the second click are stored if it is a cell
                startWall is an array where the coordinates of the first click are stored if it is a wall
                endWall is an array where the coordinates of the first click are stored if it is a wall
                previousStartColor is a variable where the colour before the first click is stored if it is a cell
                previousColorWall is a variable where the colour before the first click is stored if it is a wall
                */
                const idToRemove = document.getElementById("idToRemove").value;
                document.getElementById("comment").innerHTML = "";
                if (idToRemove !== "") {
                    if (world.removeAttribute(idToRemove)) {
                        idBlock.removeChild(document.getElementById(idToRemove));
                        document.getElementById("idToRemove").value = "";
                        document.getElementById("id").value = "";
                        return false; // allow to reset start, end, startWall, endWall
                    }
                    else {
                        document.getElementById("comment").innerHTML = "this id don't exist";
                        document.getElementById("idToRemove").value = "";
                        return false; // allow to reset start, end, startWall, endWall
                    }
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
                                return false;
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

                for (let i = 0; i < map.length; i++) {
                    for (let j = 0; j < map[0].length; j++) {
                        map[i][j] = [world.getBackgroundColor(i, j), world.isBlocked(i, j), world.getAttribute(i, j, "id")];
                    }
                }
            }
        });
        world.clearAttributeTable();
        idBlock.innerHTML = "";
        document.getElementById("comment").innerHTML = "";
        while (idBlock.firstChild) {
            idBlock.removeChild(idBlock.lastChild);
        }

        for (let i = 0; i < size * 2 + 1; i++) {
            for (let j = 0; j < size * 2 + 1; j++) {
                if (map[i][j].length === 3) {
                    world.setColorIdBlocked(i, j, map[i][j][0], map[i][j][1], map[i][j][2]);
                }
                else {
                    map[i][j] = ["white", false, null];
                    world.setColorIdBlocked(i, j, "white", false, null);
                }

            }
        }

        world.draw();

    }
    render() {
        return (
            <>
                <div>
                    <div id =  "body">
                        <div> choose the size of the grid :
                            <input
                                type="text"
                                ref={this.textInput}
                            />
                            <button onClick={this.generateGridworld}>Generate</button>
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