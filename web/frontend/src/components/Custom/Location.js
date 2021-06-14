import React from 'react';
import {Button} from "reactstrap";

function Location(props) {

    return(
        <Button onClick={props.onClick}>Location</Button>
    );
}

export default Location;