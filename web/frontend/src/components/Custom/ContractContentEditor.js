import React from "react";
import PropTypes from "prop-types";
import classnames from "classnames";
import {Button, Card, CardBody, Table} from "reactstrap";
import Input from "../Elements/Input";
import CustomSelect from "./CustomSelect";

function makeStringOf(list) {
    if (typeof list === "string") return list

    let str = ""
    for (let i=0; i<list.length-1; i++) {
        str += list[i] + ","
    }

    str += list[list.length-1]
    return str
}

const AccordionItem = ({
  title,
  color,
  content,
  defaultOpened,
  setOpen,
  changeParameter,
  addContent,
  deleteContent
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
          height: collapseStyle,
        }}
        ref={collapseRef}
      >
          <div className="text-blueGray-500 px-4 py-5 flex-auto leading-relaxed">
              <Table responsive>
                    <thead>
                    <tr>
                        <th className="text-center">Name</th>
                        <th className="text-center">Format</th>
                        <th className="text-center">Type</th>
                        <th className="text-center">Value</th>
                    </tr>
                    </thead>
                    <tbody>
                    {content.map((prop, key) => (
                        <tr key={key}>
                            <td>
                                <Input placeholder={"Name"} value={prop.name} name="subName" onChange={(e) => changeParameter(e, key)}/>
                            </td>
                            <td>
                                <Input placeholder={"Format"} value={prop.format} name="subFormat" onChange={(e) => changeParameter(e, key)}/>
                            </td>
                            <td>
                                <Input placeholder={"Type"} value={prop.type} name="subType" onChange={(e) => changeParameter(e, key)}/>
                            </td>
                            <td>
                                <Input placeholder={"Value"} value={makeStringOf(prop.value)} name="subValue" onChange={(e) => changeParameter(e, key)}/>
                            </td>
                            <td>
                                <Button
                                    className="btn-icon"
                                    color="danger"
                                    size="sm"
                                    type="button"
                                    onClick={() => deleteContent(key)}>
                                    <i className="now-ui-icons ui-1_simple-remove"/>
                                </Button>
                            </td>
                        </tr>
                    ))}
                    <tr>
                        <td colSpan="6" className="text-center">
                            <Button
                                className="btn-icon"
                                color="info"
                                size="sm"
                                type="button"
                                onClick={addContent}
                            >
                                <i className="now-ui-icons ui-1_simple-add"/>
                            </Button>
                        </td>
                    </tr>
                    </tbody>
              </Table>
          </div>
      </div>
    </>
  );
};

AccordionItem.defaultProps = {
  defaultOpened: false,
  setOpen: () => {},
};

export default function ContractContentEditor({ items, color, changeParameter, deleteContent, addContent, assumptions }) {
    /*console.log("ITEMS")
    console.log(items)*/
  const [open, setOpen] = React.useState();
  let callBackAction = (key) => {
      setOpen(key);
  };
  return (
    <>
      <div>
        <Card className="card-plain">
            <CardBody>
                <Table responsive>
                    <thead>
                    <tr>
                        <th className="text-center">#</th>
                        <th>Type</th>
                        <th>LTL Value</th>
                        <th className="text-center">Name</th>
                        <th className="text-center">Arguments</th>
                    </tr>
                    </thead>
                    <tbody>
                        {items.map((prop, key) => (
                            <tr key={key}>
                                <td className="text-center">{key+1}</td>
                                <td>
                                    <CustomSelect items={["LTL", "pattern"]} defaultValue={prop.type} name="type" changeSelector={(e, value) => changeParameter(e, assumptions, key, value)}/>
                                </td>
                                <td>
                                    <Input placeholder={"LTL Value"} value={prop.ltl_value} name="ltl_value" onChange={(e) => changeParameter(e, assumptions, key)}/>
                                </td>
                                <td className="text-center">
                                    {prop.type === "pattern" && (<Input placeholder={"Name"} value={prop.content!==undefined ? prop.content.name : ""} name="contentName" onChange={(e) => changeParameter(e, assumptions, key)}/>)}
                                </td>
                                <td className="text-center">
                                    {prop.type === "pattern" && prop.content!==undefined && (
                                    <div
                                        className="overflow-hidden relative flex flex-col min-w-0 break-words bg-white w-full mb-5 border-b border-blueGray-200">
                                        <AccordionItem
                                            title="See Arguments"
                                            content={prop.content.arguments}
                                            color={color}
                                            setOpen={() => callBackAction(key)}
                                            changeParameter={(e, subKey) => changeParameter(e, assumptions, key, false, subKey)}
                                            addContent={() => addContent(assumptions, key)}
                                            deleteContent={(subKey) => deleteContent(key, assumptions, subKey)}
                                            defaultOpened={
                                                key === open || (Array.isArray(open) && open.includes(key))
                                            }/>
                                    </div>
                                    )}
                                </td>
                                <td>
                                    <Button
                                        className="btn-icon"
                                        color="danger"
                                        size="sm"
                                        type="button"
                                        onClick={() => deleteContent(key, assumptions)}
                                    >
                                        <i className="now-ui-icons ui-1_simple-remove"/>
                                    </Button>
                                </td>
                            </tr>
                        ))}
                        <tr>
                            <td colSpan="6" className="text-center">
                                <Button
                                    className="btn-icon"
                                    color="info"
                                    size="sm"
                                    type="button"
                                    onClick={() => addContent(assumptions)}
                                >
                                    <i className="now-ui-icons ui-1_simple-add"/>
                                </Button>
                            </td>
                        </tr>
                    </tbody>
                </Table>
            </CardBody>
        </Card>
      </div>
    </>
  );
}

ContractContentEditor.defaultProps = {
  items: [],
  defaultOpened: -1,
  multiple: false,
};

ContractContentEditor.propTypes = {
  // NOTE: if you pass an array for the defaultOpened prop
  // // // then the user will be able to open multiple collapses
  // // // For example, if you want to have only the first
  // // // collapse opened, but the user can open multiple
  // // // then you can pass defaultOpened={[0]}
  // // // otherwise, you can pass defaultOpened={0}
  defaultOpened: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.arrayOf(PropTypes.number),
  ]),
  items: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string,
      description: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.arrayOf(PropTypes.string),
      ]),
    })
  ),
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
};
