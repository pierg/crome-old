import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";
import Button from "../../Elements/Button";

function SocketIoPatterns(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(0);


    const setMessageFunction = useCallback((msg) => {
        console.log(msg)
        setMessage(msg.robotic);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return

        socket.on('receive-patterns', setMessageFunction)

        return () => socket.off('receive-patterns')
    }, [socket, setMessageFunction])

    function sendMessage() {
        socket.emit('get-patterns')
    }


    return (
        <>
            <Button onClick={sendMessage}>Get Patterns</Button>
            <h1>Response:</h1>
            <p>{message}</p>
        </>);
}

export default SocketIoPatterns;
