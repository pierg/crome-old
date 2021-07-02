import React from 'react';
import {Button} from "reactstrap";

function ListLine(props) {
    return(
        <tr>
            <td>
                <i className={"text-2xl "+props.statIconName} style={{color: props.color}}/>
            </td>
            <td>
                {props.name}
            </td>
            <td className="flex justify-end pr-0">
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