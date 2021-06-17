import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../components/Crome/IndexEnvironment";
import GridWorld from "../../components/Crome/IndexEnvironment";
import Location from "../../components/Custom/Location";
import {Card, CardBody, PopoverBody, PopoverHeader, Table, UncontrolledPopover} from "reactstrap";
import img from "./robot1.png";
import * as json from "./environment_example.json";
import footeradmin from "../../_texts/admin/footers/footeradmin";
import FooterAdmin from "../../components/Footers/Admin/FooterAdmin";
import Button from "../../components/Elements/Button";
import createenvironment from "_texts/custom/createenvironment.js";

export default class CreateEnvironment extends React.Component {

    state = {
        locations: [],
        colors: [],
        numChildren: 0,
        errorMsg: "",
        warningPop: false
    }

    componentDidMount() {
        this.generateGridworld()
    }

    componentWillUnmount() {
        // fix Warning: Can't perform a React state update on an unmounted component
    }

    onAddLocation = (id, color) => {
        let tmpLocations = this.state.locations
        let tmpColors = this.state.colors

        if (!tmpLocations.includes(id)) {
            tmpLocations.push(id)
            tmpColors.push(color)

            this.setState({
                locations: tmpLocations,
                colors: tmpColors,
                numChildren: this.state.numChildren + 1
            })
        }
    }

    deleteLocation = (key) => {
        let tmpLocations = this.state.locations
        let tmpColors = this.state.colors
        let index = tmpLocations.indexOf(key)

        tmpLocations.splice(index, 1)
        tmpColors.splice(index, 1)

        this.setState({
            locations: tmpLocations,
            colors: tmpColors,
            numChildren: this.state.numChildren - 1
        })

        this.removeId(key)
    }

    deleteAllLocations = () => {
        let tmpLocations = this.state.locations

        for (let i=0; i<tmpLocations.length; i++) {
            this.removeId(tmpLocations[i])
        }

        this.setState({
            locations: [],
            colors: [],
            numChildren: 0
        })
    }

    callbackMap = (map) => {
        this.map = map
    }

    updateErrorMsg = (msg) => {
        if (msg !== "") {
            this.setState({
                errorMsg: msg,
                warningPop: true
            });
            setTimeout(() => {
                this.setState({warningPop: false});
            }, 4000)
        }
        else {
            this.setState({
                warningPop: false
            })
        }
    }

    constructor(props) {
        super(props);
        this.myCanvas = React.createRef();
        this.generateGridworld = this.generateGridworld.bind(this);
        this.generateGridworldWithJSON = this.generateGridworldWithJSON.bind(this);
        this.saveInToJSON = this.saveInToJSON.bind(this);
        this.id = React.createRef();
        this.divId = React.createRef();
        this.map = [];
        this.clearGridworld = this.clearGridworld.bind(this);
        this.removeId = this.removeId.bind(this);
        this.clearButton = React.createRef();
        this.saveButton = React.createRef();
        this.world = null;
        this.launchRobot = this.launchRobot.bind(this);
        this.robot = this.robot.bind(this);
        this.robotButton = React.createRef();
        this.size = 8;
        this.i = 0;
        this.t = null;
        this.tab = [[1,5],[1,3],[1,1],[3,1],[3,3],[5,3],[5,1],[7,1],[9,1],[9,3],[7,3],[5,3],[5,5],[3,5],[1,5]];
        this.x = null;
        this.y = null;
    }

    modifyGridSize(increment) {

        this.size += increment

        let oldMap = this.map;
        let maxIdX = 0; // table corresponding to the node with the largest x as abscissa and its colour
        let minIdX = this.map.length; // table corresponding to the node with the smallest x abscissa and its colour
        let minIdY = this.map[0].length; // table corresponding to the node with the smallest y and its colour as ordinates
        let maxIdY = 0; // table corresponding to the node with the largest x and its colour as ordinates
        for (let i = 0; i < this.map.length; i++) {
            for (let j = 0; j < this.map[0].length; j++) { // if the colour of the node is not white check if it is the point corresponding to one of the 4 ends
                if (this.map[i][j][0] !== "white") {
                    minIdX = this.end(minIdX, i, this.map[i][j][0], minIdX >= i);
                    minIdY = this.end(minIdY, j, this.map[i][j][0], minIdY >= j);
                    maxIdX = this.end(maxIdX, i, this.map[i][j][0], maxIdX <= i);
                    maxIdY = this.end(maxIdY, j, this.map[i][j][0], maxIdY <= j);
                }
            }
        }
        let oldSizeX = maxIdX - minIdX + 1;
        let oldSizeY = maxIdY - minIdY + 1;
        let isInX = (this.size * 2 + 1) - oldSizeX;
        let isInY = (this.size * 2 + 1) - oldSizeY;

        if (isInX <= 0 || isInY <= 0) {
            console.log(createenvironment)
            this.updateErrorMsg(createenvironment.errorMsg.gridTooSmall);
            this.size -= increment
        }
        else {
            let leftBorderX = Math.trunc(isInX / 2);
            let topBorderY = Math.trunc(isInY / 2);
            leftBorderX = this.shift(leftBorderX, minIdX);
            topBorderY = this.shift(topBorderY, minIdY);

            this.map = [];

            this.buildMap(this.map, this.size);

            for (let i = leftBorderX; i < leftBorderX + oldSizeX; i++) {
                for (let j = topBorderY; j < topBorderY + oldSizeY; j++) {
                    this.map[i][j] = oldMap[minIdX + i - leftBorderX][minIdY + j - topBorderY];
                }
            }

            this.world.onclick = null
            this.world = this.buildGrid(this.myCanvas.current, this.size, this.map, this.onAddLocation, this.callbackMap, this.updateErrorMsg)
        }
    }

    generateGridworld() {
        if (this.world !== null) this.world.onclick = null
        this.world = this.buildGrid(this.myCanvas.current, this.size, this.map, this.onAddLocation, this.callbackMap, this.updateErrorMsg)
    }

    generateGridworldWithJSON() {
        this.hidden();
        const locations = json.grid.locations;
        const walls = json.grid.walls;
        let  x;
        let  y;
        this.buildMap(this.map, (json.size[0].width / 2));
        for (let i = 0; i < locations.length; i++) {
            for (let j = 0; j < locations[i].coordinates.length; j++) {
                x = locations[i].coordinates[j].x * 2 - 1;
                y = locations[i].coordinates[j].y * 2 - 1;
                this.map[x][y] = [locations[i].color, true, locations[i].id];
            }
        }
        for (let i = 0; i < walls.length; i ++) {
            x = ((walls[i].left.x * 2 - 1) + (walls[i].right.x * 2 - 1)) / 2 ;
            y = ((walls[i].left.y * 2 - 1) + (walls[i].right.y * 2 - 1)) / 2 ;
            this.map[x][y] = ["black", true, null];
        }
        if (this.world !== null) this.world.onclick = null;
        this.world = this.buildGrid(this.myCanvas.current, (json.size[0].width / 2), this.map, this.onAddLocation, this.callbackMap, this.updateErrorMsg);
    }

    saveInToJSON() {
        const idTable = this.world.getIdTable();
        let obj = {filetype: "environment",
            session_id: "default",
            project_id: "simple",};
        obj.size = {width: this.size * 2, height: this.size * 2};
        obj.grid = {location : [], walls : []};
        for (let i = 0; i < idTable.length; i++) {
            obj.grid.location.push({coordinates : [], color : idTable[i][1], id : idTable[i][0]});
        }
        for (let i = 0; i < this.map.length; i++) {
            for (let j = 0; j < this.map[0].length; j++) {
                if (this.map[i][j][0] !== "white" && this.map[i][j][2] !== null) {
                    const index = this.world.isID(this.map[i][j][2]);
                    obj.grid.location[index].coordinates.push({x : Math.trunc(i / 2) + 1, y : Math.trunc(j / 2) + 1})
                }
                else if (this.map[i][j][0] === "black") {
                    obj.grid.walls.push({left : { x : i / 2, y : Math.trunc(j / 2) + 1},right : { x : (i / 2) + 1, y : Math.trunc(j / 2) + 1 }})
                }
            }
        }
        let fs = require('browserify-fs');
        const myJSON = JSON.stringify(obj);
        const name = window.prompt("What is the name of the file ?");
        fs.writeFile("./" + name + ".json", myJSON);
    }

    clearGridworld() {
        this.map = []
        this.world.clearAttributeTable()
        this.world.resetInColorTable()
        const context = this.myCanvas.current.getContext('2d')
        context.clearRect(0, 0, this.myCanvas.current.width, this.myCanvas.current.height)
        this.deleteAllLocations()
        this.world.onclick = null
        this.world = this.buildGrid(this.myCanvas.current, this.size, this.map, this.onAddLocation, this.callbackMap, this.updateErrorMsg)
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
        this.world.removeAttribute(idToRemove);
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

    buildGrid(canvas, size, map, addLocation, callbackMap, updateErrorMsg) {
        if (map.length === 0) {
            this.buildMap(map, size);
        }

        let world = new GridWorld(canvas, size, size, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true});

        this.drawRobot();

        world.onclick = function (node) {
            /*
            start is an array where the coordinates of the first click are stored if it is a cell
            end is an array where the coordinates of the second click are stored if it is a cell
            startWall is an array where the coordinates of the first click are stored if it is a wall
            endWall is an array where the coordinates of the first click are stored if it is a wall
            previousStartColor is a variable where the colour before the first click is stored if it is a cell
            previousColorWall is a variable where the colour before the first click is stored if it is a wall
            */
            updateErrorMsg("")

            let start = world.getStart();
            let startWall = world.getStartWall();
            let end = world.getEnd();
            let endWall = world.getEndWall();
            let previousStartColor = world.getPreviousStartColor();
            let previousColorWall = world.getPreviousColorWall();

            if (startWall.length !== 0 && start.length !== 0) {
                world.resetCellWall(start, startWall, previousStartColor, previousColorWall);
                return;
            }

            if (node.x % 2 === 1 && node.y % 2 === 1) { // if the user click on a cell
                if (start.length !== 0) { // when it's the second click, draw a square
                    end.push(node.x);
                    end.push(node.y);
                    let minX = world.min(start[0], end[0])[0]; // these variables allow to create only one loop for
                    let maxX = world.min(start[0], end[0])[1];
                    let maxY = world.min(start[1], end[1])[1];
                    let minY = world.min(start[1], end[1])[0];
                    let previousColorArray = [];
                    for (let i = minX; i < maxX + 1; i += 1) {
                        previousColorArray[i] = [];
                        for (let j = minY; j < maxY + 1; j += 1) {
                            previousColorArray[i].push(world.getBackgroundColor(i, j));
                            world.setBackgroundColor(i, j, "#9b9b9b");
                        }
                    }
                    previousColorArray[start[0]][start[1] - minY] = previousStartColor;
                    const answer = world.askToColor(minX, maxX, maxY, minY, previousColorArray, map);
                    if (answer !== false) {
                        const color = answer[0];
                        const id = answer[1];
                        if (document.getElementById(id) === null || document.getElementById(id).innerHTML === "") {
                            addLocation(id, color)
                        }
                    }

                } else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                    if (startWall.length !== 0) {
                        world.resetCellWall(startWall, null, previousColorWall, null);
                        return;
                    }
                    start.push(node.x);
                    start.push(node.y);
                    world.setPreviousStartColor(world.getBackgroundColor(start[0], start[1]));
                    world.setBackgroundColor(node.x, node.y, "lightgray");

                }
            } else { // when you click on wall cell
                if (startWall.length !== 0) { // when it's the second click
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
                            updateErrorMsg("you can't change the color of this wall") // TODO How can we arrive here?
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        }
                    } else if (startWall[0] === endWall[0]) { // when the users select a column
                        if (startWall[0] % 2 === 1) { // when he clicks on a case that he can't choose
                            updateErrorMsg("you have to select a row/column to change the colour of the walls") // TODO How can we arrive here?
                            world.errorMessage(startWall, previousColorWall);
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        } else {
                            min = world.min(startWall[1],endWall[1])[0];
                            max = world.min(startWall[1],endWall[1])[1];
                            for (let i = min; i < max + 1; i += 1) {
                                if ((world.isBlocked(startWall[0], i) && world.getBackgroundColor(startWall[0], i) !== "black") && previousColorWall !== "black") {// if there is a block of colour in the selected column
                                    updateErrorMsg(createenvironment.errorMsg.wallInsideBlock)
                                    world.errorMessage(startWall, previousColorWall);
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
                            updateErrorMsg("you have to select a row/column to change the colour of the walls") // TODO How can we arrive here?
                            world.errorMessage(startWall, previousColorWall);
                            world.resetCellWall(startWall, null, previousColorWall, null);
                            return;
                        } else {
                            min = world.min(startWall[0],endWall[0])[0];
                            max = world.min(startWall[0],endWall[0])[1];

                            for (let i = min; i < max + 1; i += 1) {
                                if ((world.isBlocked(i, startWall[1]) && world.getBackgroundColor(i, startWall[1]) !== "black" ) && previousColorWall !== "black") { // if there is a block of colour in the selected column
                                    updateErrorMsg(createenvironment.errorMsg.wallInsideBlock)
                                    world.errorMessage(startWall, previousColorWall);
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
                        updateErrorMsg(createenvironment.errorMsg.wallLine)
                    }
                    world.reset();
                }
                else { // when it's the first click, color the cell with a "light" color so the user know that he needs to click on a other cell
                    if (start.length !== 0) {
                        world.resetCellWall(start, null, previousStartColor, null);
                        return;
                    }
                    startWall.push(node.x);
                    startWall.push(node.y);
                    world.setPreviousColorWall(world.getBackgroundColor(startWall[0], startWall[1]));
                    if (world.getBackgroundColor(node.x, node.y) === "white" || world.getBackgroundColor(node.x, node.y) === "black") {
                        world.setBackgroundColor(node.x, node.y, "lightgray");
                    } else { // when he clicks on a case that he can't choose
                        updateErrorMsg(createenvironment.errorMsg.wallInsideBlock)
                        world.reset();
                        return;
                    }
                }
            }
            world.updateMap(map);
            callbackMap(map)
        }
        updateErrorMsg("")

        for (let i = 0; i < size * 2 + 1; i++) {
            for (let j = 0; j < size * 2 + 1; j++) {
                world.setColorIdBlocked(i, j, map[i][j][0], map[i][j][1], map[i][j][2]);
            }
        }

        return world;
    }

    render() {
        const children = [];
        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<Location key={i}
                                    name={this.state.locations[i]}
                                    onClick={() => this.deleteLocation(this.state.locations[i])}
                                    color={this.state.colors[i]}
                                    statIconName={"fas fa-square"}/>);
        }
        return (
            <>
                <div className="relative pt-32 pb-32 bg-orange-500">
                    <div className="px-4 md:px-6 mx-auto w-full">
                        <div>
                            <div className="flex flex-wrap justify-center">
                                <h1 className="display-3 title-up text-white font-semibold text-center">Build your Environment</h1>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="px-4 md:px-6 mx-auto w-full -mt-24">
                    <div className="mt-12 relative">
                        <div className="relative w-full overflow-hidden">
                            <div>
                                <div id="body" className="flex justify-center items-center">
                                    <div className="flex container px-4 justify-center">
                                        <div className="flex justify-center">
                                            <div className="flex flex-col items-center">
                                                <canvas className="shifted-canvas-margin" ref={this.myCanvas} id='canvas'/>

                                                <UncontrolledPopover
                                                    placement={window.innerWidth > 991 ? "left" : "top"}
                                                    target="canvas"
                                                    className="popover-info"
                                                    isOpen={this.state.warningPop}
                                                >
                                                    <PopoverHeader>Warning!</PopoverHeader>
                                                    <PopoverBody>
                                                        {this.state.errorMsg}
                                                    </PopoverBody>
                                                </UncontrolledPopover>

                                                <div className="m-4 px-16 pt-2 pb-2 relative flex flex-col min-w-0 break-words bg-white rounded shadow-lg">
                                                    <span className="font-semibold text-xs mb-1 text-center uppercase text-blueGray-700">Size of the Grid</span>
                                                    <div className="flex pl-2">
                                                        <Button color="red" onClick={() => this.modifyGridSize(-1)}><i className="text-xl fas fa-minus-square"/></Button>
                                                        <Button color="lightBlue" onClick={() => this.modifyGridSize(1)}><i className="text-xl fas fa-plus-square"/></Button>
                                                        {/*<Button ref={this.robotButton} onClick={this.launchRobot}>Robot</Button>*/}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="w-full lg:w-4/12 xl:w-3/12 flex-col">
                                            <div className="m-4 px-4 relative flex flex-col min-w-0 break-words bg-white rounded shadow-lg">
                                                <div className="flex flex-col justify-center">
                                                    <Card className="card-plain">
                                                        <CardBody className="overflow-x-initial">
                                                            <Table responsive>
                                                                <thead>
                                                                <tr>
                                                                    <th colSpan={3} className="title title-up text-center font-bold">Locations</th>
                                                                </tr>
                                                                </thead>
                                                                <tbody>
                                                                {children}
                                                                </tbody>
                                                            </Table>
                                                        </CardBody>
                                                    </Card>
                                                    <div className="flex flex-col pl-2 pb-3">
                                                       <Button ref={this.clearButton} color="amber" onClick={this.clearGridworld}><i className="text-xl mr-2 fas fa-trash-alt"/>Clear</Button>
                                                       <div className="mt-2"/>
                                                       <Button ref={this.saveButton} color="emerald" onClick={this.saveInToJSON}><i className="text-xl mr-2 fas fa-check-square"/>Save</Button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                    <FooterAdmin {...footeradmin} />
                </div>
            </>
        );
    }
}