function makePopper(ele) {
    let ref = ele.popperRef(); // used only for positioning

    ele.tippy = tippy(ref, { // tippy options:
        content: () => {
            let content = document.createElement('div');

            if (ele.data("type") === "goal") {
                if (ele.data("description") !== "") {
                    content.innerHTML = ele.data("description");
                }
                else{
                    content.innerHTML = "no description available";
                }
            } else {
                content.innerHTML = ele.data("type") + " operator";
            }
            return content;
        },
        trigger: 'manual' // probably want manual mode
    });
}


function render_cgt(nodes, edges) {

    var cy = (window.cy = cytoscape({
        container: document.getElementById("cy"),
        style: [
            {
                selector: "node[type='goal']",
                css: {
                    content: "data(id)",
                    "font-family": "monospace",
                    "font-size": "0.5em",
                    "text-valign": "center",
                    "text-halign": "center",
                    height: "30px",
                    width: "200px",
                    shape: "rectangle",
                    "background-color": "DodgerBlue"
                }
            },
            {
                selector: "node[type='COMPOSITION']",
                css: {
                    content: "||",
                    "font-family": "monospace",
                    "font-size": "0.7em",
                    "text-valign": "center",
                    "text-halign": "center",
                    height: "30px",
                    width: "30px",
                    shape: "circle",
                    "background-color": "MediumSeaGreen"
                }
            },
            {
                selector: "node[type='CONJUNCTION']",
                css: {
                    content: "/\\",
                    "font-family": "monospace",
                    "font-size": "0.7em",
                    "text-valign": "center",
                    "text-halign": "center",
                    height: "30px",
                    width: "30px",
                    shape: "circle",
                    "background-color": "MediumSeaGreen"
                }
            },
            {
                selector: "node[type='REFINEMENT']",
                css: {
                    content: "R",
                    "font-family": "monospace",
                    "font-size": "0.7em",
                    "text-valign": "center",
                    "text-halign": "center",
                    height: "30px",
                    width: "30px",
                    shape: "circle",
                    "background-color": "MediumSeaGreen"
                }
            },
            {
                selector: "node[type='MAPPING']",
                css: {
                    content: "M",
                    "font-family": "monospace",
                    "font-size": "0.7em",
                    "text-valign": "center",
                    "text-halign": "center",
                    height: "30px",
                    width: "30px",
                    shape: "circle",
                    "background-color": "MediumSeaGreen"
                }
            },
            {
                selector: "edge[type='input']",
                css: {
                    "curve-style": "bezier",
                    "control-point-step-size": 1,
                    "source-arrow-shape": "triangle",
                    'width': 1,
                }
            },
            {
                selector: "edge[type='refinement']",
                css: {
                    "curve-style": "bezier",
                    "control-point-step-size": 40,
                    "source-arrow-shape": "triangle-backcurve",

                }
            }
        ],

        elements: {
            nodes: nodes,
            edges: edges
        },
        layout: {
            name: "dagre"
        }
    }));

    cy.ready(function () {
        cy.nodes().forEach(function (ele) {
            makePopper(ele);
        });
    });

    cy.nodes().unbind('mouseover');
    cy.nodes().bind('mouseover', (event) => event.target.tippy.show());

    cy.nodes().unbind('mouseout');
    cy.nodes().bind('mouseout', (event) => event.target.tippy.hide());
    cy.bind('click', 'node', function (evt) {
        modal_id = '[data-remodal-id=modal_' + this.id() + ']';
        var inst = $(modal_id).remodal();
        if (typeof inst !== "undefined") {
            inst.open();
        }
    });

    // cy.elements().layout(
    //     {
    //         name: 'dagre',
    //     }).run();

}


