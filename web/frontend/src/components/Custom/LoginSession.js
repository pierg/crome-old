import React, {useRef} from 'react'
// import Input from "../../components/Elements/Input.js";
import Button from "../../components/Elements/Button.js";
import {Form} from 'react-bootstrap'
import {v4 as uuidV4} from 'uuid'

export default function LoginSession({id, onIdSubmit}) {
    const idRef = useRef()

    function handleSubmit(e) {
        e.preventDefault()

        onIdSubmit(idRef.current.value)
    }

    function createNewId() {
        onIdSubmit(uuidV4())
    }

    return (
        <>
            {/*TODO: Fix style*/}
            <p>Your Session ID is:</p>
            {id}
            <Form onSubmit={handleSubmit} className="w-100">
                <Form.Group>
                    <Form.Label>Load another session</Form.Label>
                    <Form.Control type="text" ref={idRef} required/>
                </Form.Group>
                <Button type="submit">Load</Button>
                <Button onClick={createNewId} variant="secondary">Reset</Button>
            </Form>
        </>
    )
}
