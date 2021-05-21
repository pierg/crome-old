import React from "react";
import {useLocation} from "react-router-dom";

// components
import CustomSidebar from "components/Custom/CustomSidebar";
import CustomPlayer from "../../components/Custom/CustomPlayer";

// texts as props
import customsidebar from "../../_texts/custom/customsidebar";
import custommediaplayerteaminfo from "_texts/custom/custommediaplayerteaminfo.js";
import {SocketProvider} from "../../contexts/SocketProvider";
import useLocalStorage from "../../hooks/useLocalStorage";


export default function CustomDashboard() {
    const location = useLocation();
    const [id, setId] = useLocalStorage('id')

    React.useEffect(() => {
        window.scrollTo(0, 0);
    }, [location]);
    return (
        <SocketProvider id={id}>
            <CustomSidebar {...customsidebar} currentRoute={"#" + location.pathname}/>
            <div className="relative md:ml-64 bg-blueGray-100">
                <CustomPlayer {...custommediaplayerteaminfo} />
            </div>
        </SocketProvider>
    );
}
