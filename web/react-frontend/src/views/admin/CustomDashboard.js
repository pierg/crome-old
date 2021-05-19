import React from "react";
import { useLocation } from "react-router-dom";

// components
import Sidebar from "components/Sidebar/Sidebar.js";
import NavbarSearchUser from "components/Navbars/NavbarSearchUser.js";
import HeaderStatCards from "components/Headers/Admin/HeaderStatCards.js";
//import CardChartJS from "components/Cards/Admin/CardChartJS.js";
import CardFullTable from "components/Cards/Admin/CardFullTable.js";
import FooterAdmin from "components/Footers/Admin/FooterAdmin.js";
// texts as props
import sidebar from "_texts/admin/sidebar/sidebar.js";
import navbarsearchusersettings2 from "_texts/admin/navbars/navbarsearchusersettings2.js";
import headerstatcards from "_texts/admin/headers/headerstatcards.js";
import cardchartjsdashboard1 from "_texts/admin/cards/cardchartjsdashboard1.js";
import cardchartjsdashboard2 from "_texts/admin/cards/cardchartjsdashboard2.js";
import cardfulltabledashboard1 from "_texts/admin/cards/cardfulltabledashboard1.js";
import cardfulltabledashboard2 from "_texts/admin/cards/cardfulltabledashboard2.js";
import footeradmin from "_texts/admin/footers/footeradmin.js";
import TabsF from "../../components/Tabs/TabsF";
import CustomHeader from "../../components/Headers/Admin/CustomHeader";
import customheadercards from "../../_texts/admin/headers/customheadercards";
import customsidebar from "../../_texts/admin/sidebar/customsidebar";
import ChildComponent from "../../components/Custom/ChildComponent";
import MediaPlayerTeamInfo from "../../components/MediaPlayers/MediaPlayerTeamInfo";
import custommediaplayerteaminfo from "_texts/e-commerce/mediaplayers/custommediaplayerteaminfo.js";
import CustomMediaPlayer from "../../components/Custom/CustomMediaPlayer";

export default function CustomDashboard() {
  const location = useLocation();
  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, [location]);
  return (
    <>
      <Sidebar {...customsidebar} />
      <div className="relative md:ml-64 bg-blueGray-100">
        <CustomHeader {...customheadercards} />
        <div className="px-4 md:px-6 mx-auto w-full -mt-24">
          <div className="flex flex-wrap justify-center">

            <ChildComponent
                  statTitle="Goal Name"
                  number="1"
                  statDescription="Description of the goal"
                  statContext="Context of the goal"
                  statObjectives="Objectives of the goal"
                  statIconName="fas fa-pen-square"
                  statSecondIconName="fas fa-trash-alt"
                  statIconColor="bg-lightBlue-600" />



            {/*<div className="w-full xl:w-8/12 px-4">
              {/*<CardChartJS {...cardchartjsdashboard1}

            </div>
            <div className="w-full xl:w-4/12 px-4">
              {/*<CardChartJS {...cardchartjsdashboard2}
            </div> />*/}
          </div>

          <CustomMediaPlayer {...custommediaplayerteaminfo} />


          <div className="flex flex-wrap">
            <div className="w-full xl:w-8/12 px-4">
              {/*<CardFullTable {...cardfulltabledashboard1} />*/}
            </div>
            <div className="w-full xl:w-4/12 px-4">
              {/*<CardFullTable {...cardfulltabledashboard2} />*/}
            </div>
          </div>
          <FooterAdmin {...footeradmin} />
        </div>
      </div>
    </>
  );
}
