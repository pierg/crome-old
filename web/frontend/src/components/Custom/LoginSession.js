import React, {useCallback, useEffect, useRef} from 'react'
import Button from "../../components/Elements/Button.js";
import {Form} from 'react-bootstrap'
import {v4 as uuidV4} from 'uuid'

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
