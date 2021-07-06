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
import console from "../../_texts/custom/console";


export default function CustomDashboard(props) {
    const location = useLocation();
    const [id, setId] = useLocalStorage('id');


    React.useEffect(() => {
        window.scrollTo(0, 0);
    }, [location]);
    return (
        <SocketProvider id={id}>
            <CustomSidebar {...customsidebar} currentRoute={"#" + location.pathname} id={id} setId={setId}/>
            <Console {...console} customText={false}/>
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
