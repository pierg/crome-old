import React from "react";
import { useLocation } from "react-router-dom";

// components
import Sidebar from "components/Sidebar/Sidebar.js";
import FooterAdmin from "components/Footers/Admin/FooterAdmin.js";
import CustomHeader from "../../components/Headers/Admin/CustomHeader";
import CustomPlayer from "../../components/Custom/CustomPlayer";

// texts as props
import footeradmin from "_texts/admin/footers/footeradmin.js";
import customheadercards from "../../_texts/admin/headers/customheadercards";
import customsidebar from "../../_texts/admin/sidebar/customsidebar";
import custommediaplayerteaminfo from "_texts/e-commerce/mediaplayers/custommediaplayerteaminfo.js";


export default function CustomDashboard() {
  const location = useLocation();
  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);
  return (
    <>
      <Sidebar {...customsidebar} />
      <div className="relative md:ml-64 bg-blueGray-100">
        {/*<CustomHeader {...customheadercards} />
        <div className="px-4 md:px-6 mx-auto w-full -mt-24">*/}
          {/*<div className="flex flex-wrap">



            {/*<div className="w-full xl:w-8/12 px-4">
              {/*<CardChartJS {...cardchartjsdashboard1}

            </div>
            <div className="w-full xl:w-4/12 px-4">
              {/*<CardChartJS {...cardchartjsdashboard2}
            </div> />
          </div>*/}

          <CustomPlayer {...custommediaplayerteaminfo} />


        {/*<div className="flex flex-wrap">
            <div className="w-full xl:w-8/12 px-4">
              {/*<CardFullTable {...cardfulltabledashboard1} />
            </div>
            <div className="w-full xl:w-4/12 px-4">
              {/*<CardFullTable {...cardfulltabledashboard2} />
            </div>
          </div>
          <FooterAdmin {...footeradmin} />
        </div>*/}
      </div>
    </>
  );
}
