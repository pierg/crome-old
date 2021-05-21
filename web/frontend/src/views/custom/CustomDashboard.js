import React from "react";
import { useLocation } from "react-router-dom";

// components
import Sidebar from "components/Sidebar/Sidebar.js";
import CustomPlayer from "../../components/Custom/CustomPlayer";

// texts as props
import customsidebar from "../../_texts/custom/customsidebar";
import custommediaplayerteaminfo from "_texts/custom/custommediaplayerteaminfo.js";


export default function CustomDashboard() {
  const location = useLocation();
  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);
  return (
    <>
      <Sidebar {...customsidebar} />
      <div className="relative md:ml-64 bg-blueGray-100">
          <CustomPlayer {...custommediaplayerteaminfo} />
      </div>
    </>
  );
}
