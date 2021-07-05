import React from 'react';
import {Button} from "reactstrap";
import mutexcolors from "_texts/custom/mutexcolors.js";

function ListLine(props) {
    return(
        <tr>
            <td>
                <div className="grid grid-template-2">
                    {props.colors.map((prop, key) => (
                        <i key={key} className={"text-2xl "+props.statIconName} style={{color: mutexcolors.colors[props.list][prop]}}/>
                    ))}
                </div>
            </td>
            <td className="text-break">
                {props.name}
            </td>
            <td className="whitespace-nowrap w-1 pr-0">
                <Button
                    className="btn-icon mr-1"
                    color="info"
                    size="sm"
                    type="button"
                    onClick={props.onEdit}
                >
                    <i className={props.editIconName}/>
                </Button>
                <Button
                    className="btn-icon"
                    color="danger"
                    size="sm"
                    type="button"
                    onClick={props.onDelete}
                >
                    <i className={props.deleteIconName}/>
                </Button>
            </td>
        </tr>
    );
}

export default ListLine;