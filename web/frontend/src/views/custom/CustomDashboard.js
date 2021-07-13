import React from "react";
import {useLocation} from "react-router-dom";

// components
import CustomSidebar from "components/Crome/CustomSidebar";
import CustomPlayer from "./CustomPlayer";

// texts as props
import customsidebar from "../../_texts/custom/customsidebar";
import custommediaplayerteaminfo from "_texts/custom/customplayerinfo.js";
import {SocketProvider} from "../../contexts/SocketProvider";
import useLocalStorage from "../../hooks/useLocalStorage";
import CreateEnvironment from "./CreateEnvironment";
import Console from "../../components/Crome/Console";
import consoleinfo from "../../_texts/custom/console";
import SocketIoConsoleMessage from "../../components/Custom/Examples/GetConsoleMessage";
import SocketIoEnvironment from "../../components/Custom/Examples/GetEnvironment";
import SocketSaveEnvironment from "../../components/Custom/Examples/SaveEnvironment";


export default function CustomDashboard(props) {
    const location = useLocation();
    const [id, setId] = useLocalStorage('id');
    let [message, setMessage] = React.useState("");
    let [environment, setEnvironment] = React.useState(null);
    let [savedEnvironment, setSavedEnvironment] = React.useState(null);

    function updateMessage(msg) {
        if (message === "") {
            setMessage(msg);
        }
        else {
            setMessage(message + "\n" + msg);
        }
    }
    function updateEnvironment(env) {
        setEnvironment(env);
    }
    function saveEnvironment(info, env) {
        setSavedEnvironment({"info":info, "environment":env})
    }

    React.useEffect(() => {
        window.scrollTo(0, 0);
    }, [location]);
    return (
        <SocketProvider id={id}>
            <CustomSidebar {...customsidebar} currentRoute={"#" + location.pathname} id={id} setId={setId}/>
            <Console {...consoleinfo} customText={message}/>
            <SocketIoConsoleMessage modifyMessage={(e) => updateMessage(e)}/>
            <SocketIoEnvironment modifyEnvironment={(e) => updateEnvironment(e)}/>
            <SocketSaveEnvironment session={id} world={savedEnvironment}/>
            <div className="relative xxl:ml-64 bg-blueGray-100 min-h-screen">
                {
                    {
                        'index': <CustomPlayer {...custommediaplayerteaminfo} id={id}/>,
                        'world': <CreateEnvironment environment={environment} saveEnvironment={saveEnvironment}/>,
                    }[props.page]
                }
            </div>
        </SocketProvider>
    );
}
