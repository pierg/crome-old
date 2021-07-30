import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import GridWorld from "../../components/Crome/IndexEnvironment";
import * as json from "./environment.json"
import img from "./robot1.png";
import * as jsoninfo from "./test.json"
import {Button} from "reactstrap";


export default class Synthesis extends React.Component {
    constructor(props) {
        super(props);
        this.myCanvas = React.createRef();
        this.map = [];
        this.world = null;
        this.tab = [];
        this.index = 0;
        this.timer = null;
        this.x = null;
        this.y = null;
        this.robotButton = React.createRef();
    }

    componentDidMount() {
        this.generateGridworldWithJSON();
        this.generate();
    }


    generateGridworldWithJSON() {
        //const json = this.props.world.environment
        const locations = json.grid.locations;

        let x;
        let y;
        this.map = this.buildMap(this.map, (json.size.width / 2));
        for (let i = 0; i < locations.length; i++) {
            for (let j = 0; j < locations[i].coordinates.length; j++) {
                x = locations[i].coordinates[j].x * 2 - 1;
                y = locations[i].coordinates[j].y * 2 - 1;
                this.map[x][y] = [locations[i].color, true, locations[i].id];

            }
        }

        this.displayWall("horizontal", json);
        this.displayWall("vertical", json);
        let leftColor;
        let aboveColor;

        for (let i = 1; i < json.size.width; i++) {
            for (let j = 1; j < json.size.width; j++) {
                if (i % 2 !== 1 || j % 2 !== 1) {
                    this.checkNeighbour(this.map, i, j);
                }
            }
        }
        for (let i = 2; i < json.size.width; i += 2) {
            for (let j = 2; j < json.size.width; j += 2) {
                this.checkNeighbour(this.map, i, j);
            }
        }
        for (let i = 2; i < json.size.width; i += 2) {
            aboveColor = this.map[i - 1][0][0];
            if (aboveColor === this.map[i + 1][0][0] && aboveColor !== "white") {
                this.map[i][0] = this.map[i - 1][0];
            }
        }
        for (let j = 2; j < json.size.width; j += 2) {
            leftColor = this.map[0][j - 1][0];
            if (leftColor === this.map[0][j + 1][0] && leftColor !== "white") {
                this.map[0][j] = this.map[0][j - 1];
            }
        }
        this.world = this.buildGrid(this.myCanvas.current, (json.size.width / 2), this.map);
    }

    buildMap(map, size) {
        map = [];
        for (let i = 0; i < size * 2 + 1; i++) {
            map[i] = [];
            for (let j = 0; j < size * 2 + 1; j++) {
                map[i].push(["white", false, null]);
            }
        }
        return map
    }

    displayWall(orientation) {
        const wall = json.grid.walls[orientation];
        let x;
        let y;
        let direction1;
        let direction2;
        if (orientation === "horizontal") {
            direction1 = "left";
            direction2 = "right";
        }
        else {
            direction1 = "up";
            direction2 = "down";
        }
        for (let i = 0; i < wall.length; i++) {
            x = ((wall[i][direction1].x * 2 - 1) + (wall[i][direction2].x * 2 - 1)) / 2 ;
            y = ((wall[i][direction1].y * 2 - 1) + (wall[i][direction2].y * 2 - 1)) / 2 ;
            this.map[x][y] = ["black", true, null];
        }
    }

    checkNeighbour(map, i, j) {
        const aboveColor = this.map[i - 1][j][0];
        const leftColor = this.map[i][j - 1][0];
        if (aboveColor === this.map[i + 1][j][0] && aboveColor !== "white") {
            this.map[i][j] = this.map[i - 1][j];
        } else if (leftColor === this.map[i][j + 1][0] && leftColor !== "white") {
            this.map[i][j] = this.map[i][j - 1];
        }
    }

    /* ROBOT FUNCTIONS */


    launchRobot() {
        this.timer = setInterval(this.robot, 1000);
    }

    drawRobot() {
        const line = document.getElementsByClassName("line");
        line[this.index].style.background = "yellow";
        const image = new Image();
        image.src = img;
        const ctx = document.getElementById('canvas').getContext('2d');
        this.x = Math.trunc(this.tab[this.index][0]/ 2 ) * 64 + 24;
        this.y = Math.trunc(this.tab[this.index][1]/ 2 ) * 64 + 24;
        ctx.drawImage(image, this.x, this.y, 50, 50);
    }

    robot(i) {
        const line = document.getElementsByClassName("line");
        const ctx = document.getElementById('canvas').getContext('2d');
        if (this.index === 1 && i === -1) {
            this.drawPreviousCase(ctx, 1);
        }
        line[this.index].style.background = "transparent";
        this.index += i;
        if (this.index === this.tab.length) {
            this.drawPreviousCase(ctx, 1);
            this.clear();
            return;
        }
        else if (this.index > 0) {
            this.drawPreviousCase(ctx, this.index - 1);
        }
        else if (this.index < 0) {
            this.clear();
            return;
        }
        this.drawRobot();
    }

    drawPreviousCase(ctx, index) {
        ctx.fillRect(this.x, this.y, 50, 50);
        this.world.setBackgroundColor(this.tab[index][0],this.tab[index][1],this.map[this.tab[index][0]][this.tab[index][1]][0]);
    }

    clear() {
        const line = document.getElementsByClassName("line");
        const ctx = document.getElementById('canvas').getContext('2d');
        if (this.index === this.tab.length) {
            this.drawPreviousCase(ctx, this.index - 1);
            line[this.index - 1].style.background = "transparent";
        }
        else if (this.index < 0) {
            this.drawPreviousCase(ctx, this.index + 1);
            line[this.index + 1].style.background = "transparent";
        }
        else {
            this.drawPreviousCase(ctx, this.index);
            line[this.index].style.background = "transparent";
        }

        this.index = 0;
        this.robot(0);
    }

    /* ROBOT FUNCTIONS */


    buildGrid(canvas, size, map,) {
        if (map.length === 0) {
            this.map = this.buildMap(map, size);
        }

        let world = new GridWorld(canvas, size, size, {
            padding: {top: 10, left: 10, right: 10, bottom: 60},
            resizeCanvas: true,
            drawBorder: true});

        world.onclick = function (node) {
        }
        for (let i = 0; i < size * 2 + 1; i++) {
            for (let j = 0; j < size * 2 + 1; j++) {
                world.setColorIdBlocked(i, j, map[i][j][0], map[i][j][1], map[i][j][2]);
            }
        }

        return world;
    }

    generate() {
        const simulation = jsoninfo.simulation;
        let table = "<tr> <th>t</th> <th>context</th> <th>controller</th> <th>inputs</th> <th>outputs</th> </tr>"
        for (let i = 0; i < simulation.length; i++) {
            table += "<tr class='line' ><td>" + simulation[i].t + "</td>";
            table += "<td>" + simulation[i].context + "</td>";
            table += "<td>" + simulation[i].controller + "</td>";
            table += "<td>" + simulation[i].inputs + "</td>";
            table += "<td>" + simulation[i].outputs + "</td></tr>";
            this.tab.push([simulation[i].x, simulation[i].y]);
        }
        document.getElementById("test").innerHTML = table;
    }
    render() {
        return (
            <>
                <div className="flex container px-4 justify-center" >
                    <div className="flex justify-center">
                        <div className="flex flex-col items-center">
                            <div className="w-full ml-4">
                                <canvas className="shifted-canvas-margin" ref={this.myCanvas} id='canvas'/>
                                <table id='test'/>
                            </div>
                        </div>
                    </div>

                </div>
                <div className="flex container px-4 justify-center">
                    <Button onClick={() =>this.robot(1)}>+</Button>
                    <Button onClick={() =>this.robot(-1)}>-</Button>
                    <Button onClick={() =>this.clear()}>clear</Button>
                </div>
            </>
        );
    }
}
