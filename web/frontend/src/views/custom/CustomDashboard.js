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


export default function CustomDashboard(props) {
    const location = useLocation();
    const [id, setId] = useLocalStorage('id');
    let [message, setMessage] = React.useState("");

    function updateMessage(msg) {
        if (message === "") {
            setMessage(msg);
        }
        else {
            setMessage(message + "\n" + msg);
        }
    }

    React.useEffect(() => {
        window.scrollTo(0, 0);
    }, [location]);
    return (
        <SocketProvider id={id}>
            <CustomSidebar {...customsidebar} currentRoute={"#" + location.pathname} id={id} setId={setId}/>
            <Console {...consoleinfo} customText={message}/>
            <SocketIoConsoleMessage modifyMessage={(e) => updateMessage(e)}/>
            <div className="relative xxl:ml-64 bg-blueGray-100">
                {
                    {
                        'index': <CustomPlayer {...custommediaplayerteaminfo} />,
                        'world': <CreateEnvironment/>,
                    }[props.page]
                }
            </div>
        </SocketProvider>
    );
}
