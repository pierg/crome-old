import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoConsoleMessage(props) {

    const socket = useSocket()

    const [message, setMessage] = useState("");


    const setMessageFunction = useCallback((message_received) => {
        setMessage(message_received);
    }, [setMessage])


    if (socket != null) socket.on('receive-message', setMessageFunction)


    useEffect(() => {
        if (socket == null) return

        socket.emit('test')
        /*socket.on('receive-message', setMessageFunction)

        return () => socket.off('receive-message')*/
    }, [socket, setMessageFunction])

    useEffect(() => {
        props.modifyMessage(message);
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoConsoleMessage;
