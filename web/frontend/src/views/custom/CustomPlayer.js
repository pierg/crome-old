import React from "react";
import PropTypes from "prop-types";
import classnames from "classnames";
import goalmodelinginfo from "_texts/custom/goalmodelinginfo.js";
import worldmodelinginfo from "_texts/custom/worldmodelinginfo.js";

// components
import GoalModeling from "./GoalModeling";
import CustomHeader from "../../components/Crome/CustomHeader";
import customheadercards from "../../_texts/custom/customheadercards";
import CustomFooter from "../../components/Custom/CustomFooter";
import footeradmin from "../../_texts/admin/footers/footeradmin";
import WorldModeling from "./WorldModeling";
import Analysis from "./Analysis";
import Synthesis from "./Synthesis";
import CustomNavButton from "../../components/Custom/CustomNavButton";
import {UncontrolledTooltip} from "reactstrap";
import {useSocket} from "../../contexts/SocketProvider";

export default function CustomPlayer({ items, defaultOpened, id, setWorld, setListOfWorldNames }) {
  const [open, setOpen] = React.useState(defaultOpened);
  const [oldInTransition, setOldInTransition] = React.useState(false);
  const [newInTransition, setNewInTransition] = React.useState(false);
  const [project, setProject] = React.useState(null);
  const [projectAdded, setProjectAdded] = React.useState(false);
  const [changingPage, setChangingPage] = React.useState(false);

  const [headerStates, setHeaderStates] = React.useState([true, false, false, false]);

  const socket = useSocket()

  function addProjectFromGoalModeling(projectId) {
      setProject(projectId)
      setProjectAdded(!projectAdded)
  }

  const toggleNew = (e, newOpen) => {

      if (((newOpen !== 1 || project !== 0) && (open !== 0 || newOpen !== 3) && (open !== 3 || newOpen !== 0)) && !changingPage) {


          if (open ===1 && newOpen === 2) socket.emit("process-goals", id)

          setChangingPage(true)

          for (let i = 0; i < headerStates.length; i++) {
              headerStates[i] = false;
          }
          headerStates[newOpen] = true;
          setHeaderStates(headerStates);

          e.preventDefault();
          if (!newInTransition && !oldInTransition) {
              setOldInTransition(true);
              setTimeout(function () {
                  setOpen(newOpen);
              }, 500);
              setTimeout(function () {
                  setOldInTransition(false);
                  setNewInTransition(true);
              }, 600);
              setTimeout(function () {
                  setNewInTransition(false);
                  setChangingPage(false)
              }, 1100);
          }
      }
  };



  return (
      <>
          <CustomHeader {...customheadercards} states={headerStates} />
          <div className="flex justify-evenly relative top--30">
              <div>
                  <CustomNavButton open={open} toggleNew={toggleNew} itemsLength={items.length} type={"back"}/>
              </div>
              <div id="continueArrow">
                  <CustomNavButton  open={open} toggleNew={toggleNew} itemsLength={items.length} type={"continue"} noProject={project === 0}/>
              </div>
              {(project === 0) && (<UncontrolledTooltip
                  delay={0}
                  placement="bottom"
                  target="continueArrow"
              >
                  <span>Select an Environment to continue</span>
              </UncontrolledTooltip>)}
          </div>
          <div className="px-4 md:px-6 mx-auto w-full -mt-24">
          <div className="mt-12 relative pb-32">
            <div className="relative w-full overflow-hidden">
              <div>
                {items.map((prop, key) => {
                  return (
                      <div
                          className={classnames(
                              "p-6 transform duration-300 transition-all ease-in-out mx-auto",
                              {
                                hidden: key !== open,
                                block: key === open,
                                "opacity-0 scale-95": key === open && oldInTransition,
                                "opacity-100 scale-100": key === open && newInTransition,
                              }
                          )}
                          key={key}
                      >
                        <div className="container mx-auto px-4">
                          {
                            {
                              'world': <WorldModeling id={id} setListOfWorldNames={setListOfWorldNames} projectAdded={projectAdded} project={project} setProject={setProject} setWorld={setWorld} {...worldmodelinginfo}/>,
                              'goal': <GoalModeling id={id} {...goalmodelinginfo} project={project} setProject={(project) => addProjectFromGoalModeling(project)}/>,
                              'analysis': <Analysis active={headerStates[2]}/>,
                              'synthesis': <Synthesis />
                            }[prop.component]
                          }
                        </div>
                      </div>
                  );
                })}
              </div>
            </div>
          </div>
          <CustomFooter {...footeradmin} />
        </div>
      </>
  );
}

CustomPlayer.defaultProps = {
  defaultOpened: 0,
  items: [],
};

CustomPlayer.propTypes = {
  // 0 represents the first element
  // also, you should note that
  // the number should not be lower then 0
  // or higher than the number of items - 1
  defaultOpened: PropTypes.number,
  // an array of string representing valid image sources
  items: PropTypes.arrayOf(
    PropTypes.shape({
      image: PropTypes.string,
      title: PropTypes.string,
      description: PropTypes.string,
      // props to pass to the Button element
      // NOTE: the color is default set by the color prop
      button: PropTypes.object,
      color: PropTypes.oneOf([
        "blueGray",
        "red",
        "orange",
        "amber",
        "emerald",
        "teal",
        "lightBlue",
        "indigo",
        "purple",
        "pink",
      ]),
    })
  ),
};
