import React from "react";
import { useLocation } from "react-router-dom";

// components
import CustomSidebar from "components/Custom/CustomSidebar";
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
      <CustomSidebar {...customsidebar} />
      <div className="relative md:ml-64 bg-blueGray-100">
          <CustomPlayer {...custommediaplayerteaminfo} />
      </div>
    </>
  );
}
