import React from "react";
import PropTypes from "prop-types";
import classnames from "classnames";

// components
import GoalModeling from "../../views/custom/GoalModeling";
import CustomHeader from "../Headers/Admin/CustomHeader";
import customheadercards from "../../_texts/admin/headers/customheadercards";
import FooterAdmin from "../Footers/Admin/FooterAdmin";
import footeradmin from "../../_texts/admin/footers/footeradmin";
import WorldModeling from "../../views/custom/WorldModeling";
import Analysis from "../../views/custom/Analysis";
import Synthesis from "../../views/custom/Synthesis";

export default function CustomPlayer({ items, defaultOpened }) {
  const [open, setOpen] = React.useState(defaultOpened);
  const [oldInTransition, setOldInTransition] = React.useState(false);
  const [newInTransition, setNewInTransition] = React.useState(false);

  const [headerStates, setHeaderStates] = React.useState([true, false, false, false]);

  const toggleNew = (e, newOpen) => {

    for (let i=0; i<headerStates.length; i++) {
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
      }, 1100);
    }
  };



  return (
      <>
        <CustomHeader {...customheadercards} states={headerStates} />
        <div className="px-4 md:px-6 mx-auto w-full -mt-24">
          <div className="mt-12 relative">
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
                              'world': <WorldModeling />,
                              'goal': <GoalModeling />,
                              'analysis': <Analysis />,
                              'synthesis': <Synthesis />
                            }[prop.component]
                          }
                        </div>
                      </div>
                  );
                })}
              </div>
              <div className="flex justify-center mb-12">
                <a
                    href="#pablo"
                    className="text-white text-center opacity-50 hover:opacity-100 transition-opacity duration-150 ease-linear w-12 text-xl"
                    onClick={(e) =>
                        toggleNew(e, open - 1 < 0 ? items.length - 1 : open - 1)
                    }
                >
                  <i className="text-lightBlue-500 fas fa-chevron-left"></i>
                  <span className="sr-only">Previous</span>
                </a>
                <a
                    href="#pablo"
                    className="text-white text-center opacity-50 hover:opacity-100 transition-opacity duration-150 ease-linear w-12 text-xl"
                    onClick={(e) =>
                        toggleNew(e, open + 1 > items.length - 1 ? 0 : open + 1)
                    }
                >
                  <i className="text-lightBlue-500 fas fa-chevron-right"></i>
                  <span className="sr-only">Next</span>
                </a>
              </div>
            </div>
          </div>
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
