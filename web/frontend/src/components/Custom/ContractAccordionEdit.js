import React from "react";
import {UncontrolledTooltip} from "reactstrap";
import Input from "../Elements/Input";
import makeStringOf from "hooks/listToStringConversion.js";

const ContractAccordionEdit = ({
  content,
  changeParameter,
  number
}) => {
  return (
      <>
        {content.map((prop, key) => (
            <div className="flex items-center">
              <div className="mr-4">{prop.name[0].toUpperCase()+prop.name.slice(1)+" : "}</div>

              <Input id={"tooltipValues"+number+key} autoComplete="off" placeholder={"Value"} value={makeStringOf(prop.value)} name="subValue" onChange={(e) => changeParameter(e, key)}/>
              {prop.format === "list" && (
                  <UncontrolledTooltip
                      delay={100}
                      placement="bottom"
                      target={"tooltipValues"+number+key}
                  >
                    To enter several values, separate them with ","
                  </UncontrolledTooltip>
              )}
            </div>))}
      </
>
  );
};
export default ContractAccordionEdit;