import React from "react";
import classnames from "classnames";
import {Table} from "reactstrap";
import makeStringOf from "hooks/listToStringConversion.js";
import searchPatterns from "hooks/searchPatterns.js";

const ContractAccordionItem = ({
  title,
  color,
  content,
  defaultOpened,
  setOpen,
  patterns
}) => {
  const [collapseOpen, setCollapseOpen] = React.useState(defaultOpened);
  const [rotate, setRotate] = React.useState(defaultOpened);
  const [collapseStyle, setCollapseStyle] = React.useState(undefined);
  const [animation, setAnimation] = React.useState(false);
  const collapseRef = React.useRef(null);
  const openAnimation = () => {
    setOpen();
    if (!collapseOpen && collapseStyle === undefined) {
      setCollapseStyle(0);
    }
    setCollapseOpen(true);
    setTimeout(function () {
      setCollapseStyle(collapseRef.current.scrollHeight);
    }, 10);
    setTimeout(function () {
      setAnimation(false);
    }, 310);
  };
  const closeAnimation = () => {
    let timeOutTime = 0;
    if (collapseOpen && collapseStyle === undefined) {
      setCollapseStyle(collapseRef.current.scrollHeight);
      timeOutTime = 10;
    }
    setTimeout(function () {
      setCollapseStyle(0);
    }, timeOutTime);
    setTimeout(function () {
      setAnimation(false);
      setCollapseOpen(false);
    }, 310);
  };
  const startAnitmation = (e) => {
    e.preventDefault();
    if (!animation) {
      setAnimation(true);
      setRotate(!rotate);
      if (collapseOpen) {
        closeAnimation();
      } else {
        openAnimation();
      }
    }
  };
  React.useEffect(() => {
    if (!defaultOpened) {
      setCollapseStyle(collapseRef.current.scrollHeight);
      setRotate(false);
      setTimeout(function () {
        setCollapseStyle(0);
      }, 10);
      setTimeout(function () {
        setAnimation(false);
        setCollapseOpen(false);
      }, 310);
    }
  }, [defaultOpened]);

  const colors = {
    blueGray: "text-blueGray-700 hover:text-blueGray-900",
    red: "text-red-500 hover:text-red-700",
    orange: "text-orange-500 hover:text-orange-700",
    amber: "text-amber-500 hover:text-amber-700",
    emerald: "text-emerald-500 hover:text-emerald-700",
    teal: "text-teal-500 hover:text-teal-700",
    lightBlue: "text-lightBlue-500 hover:text-lightBlue-700",
    indigo: "text-indigo-500 hover:text-indigo-700",
    purple: "text-purple-500 hover:text-purple-700",
    pink: "text-pink-500 hover:text-pink-700",
  };

  return (
    <>
      <div className="bg-transparent first:rounded-t px-4 py-3">
        <a href="#openCollapse" onClick={startAnitmation}>
          <h5
            className={
              colors[color] +
              " mb-0 font-semibold duration-300 transition-all ease-in-out"
            }
          >
            {title}
              <i
                  className={classnames(
                      "text-sm mr-2 float-right fas fa-chevron-down duration-300 transition-all ease-in-out transform",
                      {"rotate-180": rotate}
                  )}
              />
          </h5>
        </a>
      </div>
      <div
        className={classnames("duration-300 transition-all ease-in-out", {
          block: collapseOpen,
          hidden: !collapseOpen,
        })}
        style={{
            height: "auto",
            maxHeight: collapseStyle,
        }}
        ref={collapseRef}
      >
          <div className="text-blueGray-500 px-4 py-5 flex-auto leading-relaxed">
              <Table responsive>
                    <thead>
                    <tr>
                        <th className={"title-up"}>LTL Value</th>
                        <th className={"title-up"}>Pattern</th>
                    </tr>
                    </thead>
                    <tbody>
                    {/*console.log(content)*/}
                    {content.map((prop, key) => (

                        <tr key={key}>
                            {/*(key===0) ? console.log(content) : ""*/}
                            <td colSpan={prop.pattern !== undefined ? 1 : 2}><p>{prop.ltl_value}</p></td>
                            {prop.pattern !== undefined && (
                                <td>
                                    <p>{prop.pattern.name}</p>
                                    {searchPatterns(prop.pattern, patterns).map((arg, subKey) => (
                                        <p key={subKey}>{arg.name+" : "+makeStringOf(arg.value)}</p>
                                    ))}
                                </td>
                            )}
                        </tr>
                    ))}
                    </tbody>
              </Table>
          </div>
      </div>
    </>
  );
};

ContractAccordionItem.defaultProps = {
  defaultOpened: false,
  setOpen: () => {},
};

export default ContractAccordionItem;