import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoConsoleMessage(props) {

    const socket = useSocket()

    const [message, setMessage] = useState("");


    const setMessageFunction = useCallback((message_received) => {
        console.log("message_received")
        //console.log(message_received)
        setMessage(message_received);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return

        socket.emit('test')
        socket.on('receive-message', setMessageFunction)

        return () => socket.off('receive-message')
    }, [socket, setMessageFunction])

    useEffect(() => {
        console.log("sending")
        console.log(message)
        props.modifyMessage(message);
        console.log(message)


    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoConsoleMessage;
