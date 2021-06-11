import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../components/Crome/IndexEnvironment";
import GridWorld from "../../components/Crome/IndexEnvironment";
import img from "./robot1.png";

export default class CreateEnvironment extends React.Component {

    constructor(props) {
        super(props);
        this.myCanvas = React.createRef();
        this.textInputSize = React.createRef();
        this.colorComponent = React.createRef();
        this.generateGridworld = this.generateGridworld.bind(this);
        this.id = React.createRef();
        this.idBlock = React.createRef();
        this.divId = React.createRef();
        this.map = [];
        this.clearGridworld = this.clearGridworld.bind(this);
        this.removeId = this.removeId.bind(this);
        this.clearButton = React.createRef();
        this.world = null;
        this.launchRobot = this.launchRobot.bind(this);
        this.robot = this.robot.bind(this);
        this.robotButton = React.createRef();
        this.i = 0;
        this.t = null;
        this.tab = [[1,5],[1,3],[1,1],[3,1],[3,3],[5,3],[5,1],[7,1],[9,1],[9,3],[7,3],[5,3],[5,5],[3,5],[1,5]];
        this.x = null;
        this.y = null;
    }

    generateGridworld() {
        this.colorComponent.current.hidden = false;
        this.divId.current.hidden = false;
        this.clearButton.current.hidden = false;
        this.robotButton.current.hidden = false;
        this.world = this.buildGrid(this.myCanvas.current, this.textInputSize.current.value,this.id.current, this.idBlock.current, this.map);
    }

    clearGridworld() {
        this.map = [];
        const context = this.myCanvas.current.getContext('2d');
        context.clearRect(0, 0, this.myCanvas.current.width, this.myCanvas.current.height);
        this.idBlock.current.innerHTML = "";
        while (this.idBlock.current.firstChild) {
            this.idBlock.current.removeChild(this.idBlock.current.lastChild);
        }
        this.buildGrid(this.myCanvas.current, this.textInputSize.current.value,this.id.current, this.idBlock.current, this.map);
    }
    launchRobot() {
        this.t = setInterval(this.robot, 1000);
    }
    robot() {
        const ctx = document.getElementById('canvas').getContext('2d');
        if (this.i === this.tab.length) {
            clearInterval(this.t);
            this.i = 0;
            return;
        }
        else if (this.i > 0) {
            ctx.fillRect(this.x, this.y, 50, 50);
            this.world.setBackgroundColor(this.tab[this.i - 1][0],this.tab[this.i - 1][1],this.map[this.tab[this.i - 1][0]][this.tab[this.i - 1][1]][0]);
        }
        this.drawRobot();
        this.i++;
    }

    drawRobot() {
        const image = new Image();
        image.src = img;
        const ctx = document.getElementById('canvas').getContext('2d');
        this.x = Math.trunc(this.tab[this.i][0]/ 2 ) * 64 + 24;
        this.y = Math.trunc(this.tab[this.i][1]/ 2 ) * 64 + 24;
        ctx.drawImage(image, this.x, this.y, 50, 50);
    }

    removeId(idToRemove) {
        console.log("test");
        this.world.removeAttribute(idToRemove);
        this.idBlock.current.removeChild(document.getElementById(idToRemove));
        document.getElementById("idToRemove").value = "";
        document.getElementById("id").value = "";
        this.world.updateMap(this.map);
        this.world.reset();
    }

    buildMap(map, size) {
        for (let i = 0; i < size * 2 + 1; i++) {
            map[i] = [];
            for (let j = 0; j < size * 2 + 1; j++) {
                map[i].push(["white", false, null]);
            }
        }
    }
    end(a, i, color, bool) {
        if (bool && (a !== i || color !== "black")) { // if there are several points corresponding to one end, the one that does not have the colour black is chosen
            a = i;
        }
        return a;
    }

    shift(border, index) {
        if (border % 2 !== index % 2) border++;
        return border;
    }

    buildGrid(canvas, size, idInput, idBlock, map) {
        if (map.length === 0) {
            this.buildMap(map, size);
        }
        else {
            let map2 = map;
            let maxIdX = 0; // table corresponding to the node with the largest x as abscissa and its colour
            let minIdX = map.length; // table corresponding to the node with the smallest x abscissa and its colour
            let minIdY = map[0].length; // table corresponding to the node with the smallest y and its colour as ordinates
            let maxIdY = 0; // table corresponding to the node with the largest x and its colour as ordinates
            for (let i = 0; i < map.length; i++) {
                for (let j = 0; j < map[0].length; j++) { // if the colour of the node is not white check if it is the point corresponding to one of the 4 ends
                    if (map[i][j][0] !== "white") {
                        minIdX = this.end(minIdX, i, map[i][j][0], minIdX >= i);
                        minIdY = this.end(minIdY, j, map[i][j][0], minIdY >= j);
                        maxIdX = this.end(maxIdX, i, map[i][j][0], maxIdX <= i);
                        maxIdY = this.end(maxIdY, j, map[i][j][0], maxIdY <= j);
                    }
                }
            }
            let oldSizeX = maxIdX - minIdX + 1;
            let oldSizeY = maxIdY - minIdY + 1;
            let isInX = (size * 2 + 1) - oldSizeX;
            let isInY = (size * 2 + 1) - oldSizeY;

            if (isInX < 0 || isInY < 0) {
                console.log("the retracted size is too small compared to the block, choose another size or clear before");
                size = Math.trunc(map.length/2);
            }
            else {
                let leftBorderX = Math.trunc(isInX / 2);
                let topBorderY = Math.trunc(isInY / 2);
                leftBorderX = this.shift(leftBorderX, minIdX);
                topBorderY = this.shift(topBorderY, minIdY);

                map = [];

                this.buildMap(map, size);

                for (let i = leftBorderX; i < leftBorderX + oldSizeX; i++) {
                    for (let j = topBorderY; j < topBorderY + oldSizeY; j++) {
                        map[i][j] = map2[minIdX + i - leftBorderX][minIdY + j - topBorderY];
                    }
                }
            }
        }

        let world = new GridWorld(canvas, size, size, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true});

        world.onclick = function (node) {
            /*
            start is an array where the coordinates of the first click are stored if it is a cell
            end is an array where the coordinates of the second click are stored if it is a cell
            startWall is an array where the coordinates of the first click are stored if it is a wall
            endWall is an array where the coordinates of the first click are stored if it is a wall
            previousStartColor is a variable where the colour before the first click is stored if it is a cell
            previousColorWall is a variable where the colour before the first click is stored if it is a wall
            */
            document.getElementById("comment").innerHTML = "";

            let start = world.getStart();
            let startWall = world.getStartWall();
            let end = world.getEnd();
            let endWall = world.getEndWall();
            let previousStartColor = world.getPreviousStartColor();
            let previousColorWall = world.getPreviousColorWall();
            const idToRemove = document.getElementById("idToRemove").value;
            const id = idInput.value;
            const selectColor = document.getElementById("color");
            const choiceColor = selectColor.selectedIndex;  // Take the index of the chosen <option>
            const color = selectColor.options[choiceColor].text;

            if (idToRemove !== "") {
                if (world.removeAttribute(idToRemove)) {
                    idBlock.removeChild(document.getElementById(idToRemove));
                    document.getElementById("idToRemove").value = "";
                    document.getElementById("id").value = "";
                    world.updateMap(map);
                    world.reset();
                    return ; // allow to reset start, end, startWall, endWall
                }
                else {
                    document.getElementById("comment").innerHTML = "this id doesn't exist";
                    document.getElementById("idToRemove").value = "";
                    world.reset();
                    return; // allow to reset start, end, startWall, endWall
                }
            }
            if (startWall.length !== 0 && start.length !== 0) {
                world.resetCellWall(start, startWall, previousStartColor, previousColorWall);
                return;
            }

            if (node.x % 2 === 1 && node.y % 2 === 1) { // if the user click on a cell
                if (start.length !== 0) { // when it's the second click, draw a square
                    end.push(node.x);
                    end.push(node.y);
                    if (id === "") { // when the user didn't input an id
                        world.errorMessage(document.getElementById("comment"), start, previousStartColor, "you need to put an id");
                        world.resetCellWall(start, null, previousStartColor, null);
                        return;
                    }
                    else if (world.isAttribute(id, color) === true) { // when the user input an id that is already use
                        world.errorMessage(document.getElementById("comment"), start, previousStartColor, "id or color already use");
                        world.resetCellWall(start, null, previousStartColor, null);
                        return;
                    }
                    else {

                        let minX = world.min(start[0], end[0])[0]; // these variables allow to create only one loop for
                        let maxX = world.min(start[0], end[0])[1];
                        let maxY = world.min(start[1], end[1])[1];
                        let minY = world.min(start[1], end[1])[0];
                        for (let i = minX; i < maxX + 1; i += 1) {
                            for (let j = minY; j < maxY + 1; j += 1) {
                                world.checkNeighbour(i, j, color); //if the cell has already a color, color his neighbors in white except if there is a wall
                                world.setColorIdBlocked(i, j, color, true, id);
                            }
                        }
                        world.reset();
                        if (document.getElementById(id) === null || document.getElementById(id).innerHTML === "") {
                            idBlock.innerHTML += "<div id=" + id + ">Color : " + color + " , id :" + id + "<button onClick = {this.removeId( " + id + ")}>Remove</button></div>";
                        }
                    }
                } else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                    start.push(node.x);
                    start.push(node.y);
                    world.setPreviousStartColor(world.getBackgroundColor(start[0], start[1]));

                    if (id === "") { // when the user didn't input an id
                        document.getElementById("comment").innerHTML = "you need to put an id";
                        if (startWall.length !== 0) {
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        }
                        world.reset();
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
                if (startWall.length !== 0) {// when it's the second click
                    endWall.push(node.x);
                    endWall.push(node.y);
                    let min;
                    let max;

                    if (startWall[0] === endWall[0] && startWall[1] === endWall[1]) { // when you double-click on a wall
                        if (previousColorWall === "black") { // if the wall was black the background color will be white
                            world.setColorIdBlocked(startWall[0], startWall[1], "white", false, null);
                            return;
                        } else if (previousColorWall === "white" || previousColorWall === null) { // if the wall was white the background color will be black
                            world.setColorIdBlocked(startWall[0], startWall[1], "black", true, null);
                            return;
                        } else { // if the wall was neither black nor white, you can't change the background color
                            document.getElementById("comment").innerHTML = "you can't change the color of this wall";
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        }
                    } else if (startWall[0] === endWall[0]) { // when the users select a column
                        if (startWall[0] % 2 === 1) { // when he clicks on a case that he can't choose
                            world.errorMessage(document.getElementById("comment"), startWall, previousColorWall, "you have to select a row/column to change the colour of the walls");
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        } else {
                            min = world.min(startWall[1],endWall[1])[0];
                            max = world.min(startWall[1],endWall[1])[1];
                            for (let i = min; i < max + 1; i += 1) {
                                if ((world.isBlocked(startWall[0], i) && world.getBackgroundColor(startWall[0], i) !== "black") && previousColorWall !== "black") {// if there is a block of colour in the selected column
                                    world.errorMessage(document.getElementById("comment"), startWall, previousColorWall, "you cannot select these, there are wall inside a block");
                                    world.resetCellWall(startWall, null, previousColorWall, null);
                                    return;
                                }
                            }
                            for (let i = min; i < max +1; i+= 1) {
                                world.setBackgroundColorWall(startWall[0], i, previousColorWall);
                            }
                        }
                    } else if (startWall[1] === endWall[1]) { // when the users select a line
                        if (startWall[1] % 2 === 1) { // when he clicks on a case that he can't choose
                            world.errorMessage(document.getElementById("comment"), startWall, previousColorWall, "you have to select a row/column to change the colour of the walls");
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        } else {
                            min = world.min(startWall[0],endWall[0])[0];
                            max = world.min(startWall[0],endWall[0])[1];

                            for (let i = min; i < max + 1; i += 1) {
                                if ((world.isBlocked(i, startWall[1]) && world.getBackgroundColor(i, startWall[1]) !== "black" ) && previousColorWall !== "black") { // if there is a block of colour in the selected column
                                    world.errorMessage(document.getElementById("comment"), startWall, previousColorWall, "you cannot select these, there are wall inside a block");
                                    world.resetCellWall(startWall, null, previousColorWall, null);
                                    return;
                                }
                            }
                            for (let i = min; i < max +1; i+= 1) {
                                world.setBackgroundColorWall(i, startWall[1], previousColorWall);
                            }
                        }
                    } else {
                        world.setBackgroundColor(startWall[0], startWall[1], "white");
                        document.getElementById("comment").innerHTML = "select a line or a column when you want to put wall";
                    }
                    world.reset();
                }
                else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                    startWall.push(node.x);
                    startWall.push(node.y);
                    world.setPreviousColorWall(world.getBackgroundColor(startWall[0], startWall[1]));
                    if (world.getBackgroundColor(node.x, node.y) === "white" || world.getBackgroundColor(node.x, node.y) === "black") {
                        world.setBackgroundColor(node.x, node.y, "lightgray");
                    } else { // when he clicks on a case that he can't choose
                        document.getElementById("comment").innerHTML = "you cannot select a wall within a block";
                        world.reset();
                        return;
                    }
                }
            }
            world.updateMap(map);
        }

        world.clearAttributeTable();
        this.drawRobot();
        document.getElementById("comment").innerHTML = "";

        for (let i = 0; i < size * 2 + 1; i++) {
            for (let j = 0; j < size * 2 + 1; j++) {
                world.setColorIdBlocked(i, j, map[i][j][0], map[i][j][1], map[i][j][2]);
            }
        }

        return world;
    }

    render() {
        return (
            <>
                <div>
                    <div id ="body" onLoad={this.generateGridworld}>
                        <div> choose the size of the grid :
                            <input type="text" ref={this.textInputSize} />
                            <button onClick={this.generateGridworld}>Generate</button>
                            <button ref={this.clearButton} hidden={true} onClick={this.clearGridworld}>Clear</button>
                            <button ref={this.robotButton} hidden={true} onClick={this.launchRobot}>Robot</button>
                        </div>
                        <canvas ref={this.myCanvas} id='canvas'/>
                        <select ref={this.colorComponent} hidden={true} id="color" name="color">
                            <option>blue</option>
                            <option>red</option>
                            <option>green</option>
                            <option>pink</option>
                            <option>purple</option>
                            <option>yellow</option>
                            <option>grey</option>
                        </select>
                        <input id={"id"} ref={this.id}/>
                        <div ref={this.divId} hidden={true}> choose an id to remove :
                            <input id={"idToRemove"} type="text"/>
                        </div>
                        <div id={"comment"}/>
                        <div ref={this.idBlock}/>
                    </div>
                </div>
            </>
        );
    }
}