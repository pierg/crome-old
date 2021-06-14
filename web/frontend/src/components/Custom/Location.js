import React from 'react';
import {Button} from "reactstrap";

function Location(props) {
    return(
        <tr>
            <td>
                {props.name}
            </td>
            <td>
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