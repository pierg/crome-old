import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import FetchTime from "../../components/Custom/Examples/FetchTime";
import SocketIoMessage from "../../components/Custom/Examples/SocketIoMessage";
import SocketIoPatterns from "../../components/Custom/Examples/GetPatterns";



export default class Synthesis extends React.Component {

    componentDidMount() {
        this.generate();
    }

    generate() {
        /*const simulation = json.simulation;
        let table = "<tr> <th>t</th> <th>context</th> <th>controller</th> <th>inputs</th> <th>outputs</th> </tr>"
        for (let i = 0; i < simulation.length; i++) {
            table += "<tr><td>" + simulation[i].t + "</td>";
            table += "<td>" + simulation[i].context + "</td>";
            table += "<td>" + simulation[i].controller + "</td>";
            table += "<td>" + simulation[i].inputs + "</td>";
            table += "<td>" + simulation[i].outputs + "</td></tr>";
        }
        document.getElementById("test").innerHTML = table; */
    }
    render() {
        return (
            <>
                <FetchTime/>
                <SocketIoMessage/>
                <SocketIoPatterns/>
                <div>This is Synthesis</div>
            </>
        );
    }
}
