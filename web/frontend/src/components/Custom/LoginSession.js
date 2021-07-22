import React, {useCallback, useEffect, useRef, useState} from 'react'
import Button from "../../components/Elements/Button.js";
import {Form} from 'react-bootstrap'
import {v4 as uuidV4} from 'uuid'
import {UncontrolledTooltip} from "reactstrap";

export default function LoginSession({id, onIdSubmit}) {
    const idRef = useRef()

    function handleSubmit(e) {
        e.preventDefault()

        onIdSubmit(idRef.current.value)
    }
    
    const createNewId = useCallback(() => {
        onIdSubmit(uuidV4())
    }, [onIdSubmit])
    
    useEffect(() => {
        if (id === undefined) {
            createNewId()
        }
    }, [createNewId, id])

    const [toolTipText, setToolTipText] = useState(true);
    const [toolTipColor, setToolTipColor] = useState("text-lightBlue-700");

    const toggleToolTipText = (reset) => {
        if (toolTipText !== reset) setToolTipText(reset)
        if (!reset) {
            setToolTipColor("text-white")
            setTimeout(function () {
                setToolTipColor("text-lightBlue-700")
            }, 200)
        }
    }

    return (
        <>
            <p className="text-center mt-4">Your Session ID is:</p>
            <p className={"text-center font-semibold hover:text-lightBlue-500 cursor-pointer transition-all duration-300 ease-in-out "+toolTipColor}
               onClick={() => {navigator.clipboard.writeText(id).then(() => toggleToolTipText(false))}}
               id={"idDisplay"}
               onMouseOut={() => setTimeout(function() {toggleToolTipText(true)},500)}>
                {id.split("-")[0]+"-"+id.split("-")[1]+"..."}
            </p>
            <UncontrolledTooltip
                delay={0}
                placement="bottom"
                target="idDisplay"
                className="dark-tooltip"
            >
                <div>{toolTipText ? "Click to Copy ID" : "ID Copied!"}</div>
            </UncontrolledTooltip>
            <Form onSubmit={handleSubmit} className="w-full mt-4">
                <Form.Group>
                    <Form.Control type="text" className="border-lightBlue-200" ref={idRef} required placeholder={"Load another session"}/>
                </Form.Group>
                <div className="flex w-full justify-center">
                    <Button onClick={createNewId} color="teal" variant="secondary" type="reset">Reset</Button>
                    <Button type="submit" color="lightBlue">Load</Button>
                </div>
            </Form>
        </>
    )
}
