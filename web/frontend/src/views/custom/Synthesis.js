import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import FetchTime from "../../components/Custom/Examples/FetchTime";
import SocketIoMessage from "../../components/Custom/Examples/SocketIoMessage";
import SocketIoPatterns from "../../components/Custom/Examples/GetPatterns";



export default class Synthesis extends React.Component {

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
