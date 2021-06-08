import React from "react";
import PropTypes from "prop-types";
import CustomSelect from "./CustomSelect";
import ContractAccordionItem from "./ContractAccordionItem.js";
import {Button, Card, CardBody, Table} from "reactstrap";
import Input from "../Elements/Input";

function NamesOf(obj) {
    let list = []
    for (let i=0; i<obj.length; i++) {
        list.push(obj[i].name)
    }
    return list
}

export default function ContractContentEditor({ items, patterns, color, changeParameter, deleteContent, addContent, assumptions, infos }) {
  const [open, setOpen] = React.useState();

  function searchPatterns(content) {
    for (let i=0; i<patterns.length; i++) {
        if (patterns[i].name === content.name) {
            let patternArgs = patterns[i].arguments
            for (let j=0; j<patternArgs.length; j++) {
                patternArgs[j].value = content.arguments[j] === undefined ? "" : content.arguments[j].value
            }
            return patternArgs
        }
    }
    return []
  }

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
                        {infos.titles.map((prop, key) => (
                            <th key={key}>{prop}</th>
                        ))}
                    </tr>
                    </thead>
                    <tbody>
                        {items.map((prop, key) => (
                            <tr key={key}>
                                <td>{key+1}</td>
                                <td>
                                    <CustomSelect
                                        items={infos.types}
                                        defaultValue={prop.pattern === undefined ? infos.types[0] : infos.types[1]}
                                        name="type"
                                        changeSelector={(e, value) => changeParameter(e, assumptions, key, value)}/>
                                </td>
                                <td>
                                    {prop.pattern === undefined && (<Input
                                                                        value={prop.ltl_value}
                                                                        name="ltl_value"
                                                                        onChange={(e) => changeParameter(e, assumptions, key)}/>)}
                                    {prop.pattern !== undefined && (<CustomSelect
                                                                        items={NamesOf(patterns)}
                                                                        placeholder={infos.placeholders.pattern}
                                                                        defaultValue={prop.pattern.name}
                                                                        name="contentName"
                                                                        changeSelector={(e, value) => changeParameter(e, assumptions, key, value)}/>)}
                                </td>
                                <td className="text-center">
                                    {prop.pattern !== undefined && (
                                    <div
                                        className="overflow-hidden relative flex flex-col min-w-0 break-words bg-white w-full mb-5 border-b border-blueGray-200">
                                        <ContractAccordionItem
                                            title={infos.details}
                                            content={searchPatterns(prop.pattern)}
                                            color={color}
                                            setOpen={() => callBackAction(key)}
                                            changeParameter={(e, subKey) => changeParameter(e, assumptions, key, false, subKey)}
                                            number={key}
                                            defaultOpened={key === open}/>
                                    </div>
                                    )}
                                </td>
                                <td>
                                    {prop.pattern !== undefined && (<Input
                                                                        placeholder={infos.placeholders.optLTL}
                                                                        value={prop.ltl_value}
                                                                        name="ltl_value"
                                                                        onChange={(e) => changeParameter(e, assumptions, key)}/>)}
                                </td>
                                <td>
                                    <Button
                                        className="btn-icon"
                                        color={infos.deleteButton.color}
                                        size="sm"
                                        type="button"
                                        onClick={() => deleteContent(key, assumptions)}
                                    >
                                        <i className={infos.deleteButton.icon}/>
                                    </Button>
                                </td>
                            </tr>
                        ))}
                        <tr>
                            <td colSpan="6" className="text-center">
                                <Button
                                    className="btn-icon"
                                    color={infos.addRowButton.color}
                                    size="sm"
                                    type="button"
                                    onClick={() => addContent(assumptions)}
                                >
                                    <i className={infos.addRowButton.icon}/>
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
