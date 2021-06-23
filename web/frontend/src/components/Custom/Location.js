import React from 'react';
import {Button} from "reactstrap";

function Location(props) {
    return(
        <tr>
            <td>
                <i className={"text-2xl "+props.statIconName} style={{color: props.color}}/>
            </td>
            <td className="text-center">
                {props.name}
            </td>
            <td className="flex justify-end">
                <Button
                    className="btn-icon"
                    color={"danger"}
                    size="sm"
                    type="button"
                    onClick={props.onClick}
                >
                    <i className="now-ui-icons ui-1_simple-remove"/>
                </Button>
            </td>
        </tr>
    );
}

export default Location;