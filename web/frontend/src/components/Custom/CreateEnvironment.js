import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "./indexEnvironment";
import GridWorld from "./indexEnvironment";

export default class CreateEnvironment extends React.Component {

    constructor(props) {
        super(props);
        this.myRef = React.createRef();
        this.textInput = React.createRef();
        this.colorComponent = React.createRef();
        this.idComponent = React.createRef();
        this.focusTextInput = this.focusTextInput.bind(this);

    }

    focusTextInput() {
        // Donne explicitement le focus au champ texte en utilisant l’API DOM native.
        // Remarque : nous utilisons `current` pour cibler le nœud DOM
        this.textInput.current.focus();
        this.buildGrid(this.myRef.current, this.textInput.current.value);
        this.colorComponent.current.hidden = false;
        this.idComponent.current.hidden = false;
    }

    buildGrid(canvas, size) {
        // Update the document title using the browser API

        //let canvas= myCanvas;
        console.log(size);
        let map = [];

        for (let i = 0; i < size; i++) {
            map[i] = [];
            for (let j = 0; j < size; j++) {

                map[i].push(0);
                console.log(map[i]);
            }
        }

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
            <div>
                <canvas ref={this.myRef} id='canvas' width='920' height='640'/>
                <select ref={this.colorComponent} id="color" hidden={true} name="color">
                    <option>blue</option>
                    <option>green</option>
                    <option>red</option>
                    <option>pink</option>
                    <option>purple</option>
                    <option>yellow</option>
                    <option>grey</option>
                    <option>white</option>
                </select>
                <select ref={this.idComponent} id="id" hidden={true} name="id">
                    <option/>
                    <option>a1</option>
                    <option>a2</option>
                    <option>a3</option>
                    <option>a4</option>
                    <option>b1</option>
                    <option>b2</option>
                    <option>b3</option>
                    <option>b4</option>
                    <option>c1</option>
                    <option>c2</option>
                    <option>c3</option>
                    <option>c4</option>
                    <option>h1</option>
                    <option>h2</option>
                    <option>h3</option>
                    <option>h4</option>
                    <option>k1</option>
                    <option>k2</option>
                    <option>k3</option>
                    <option>k4</option>
                    <option>l1</option>
                    <option>l2</option>
                    <option>l3</option>
                    <option>l4</option>
                    <option>l5</option>
                    <option>l6</option>
                    <option>l7</option>
                    <option>l8</option>
                    <option>r1</option>
                    <option>r2</option>
                    <option>r3</option>
                    <option>r4</option>
                </select>
                <div>
                    <input
                        type="text"
                        ref={this.textInput} />    <input
                    type="button"
                    value="Size"
                    onClick={this.focusTextInput}
                />
                </div>
            </div>

        );
    }
}


