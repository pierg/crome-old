import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoConsoleMessage(props) {

    const socket = useSocket()

    const [message, setMessage] = useState("");

    const setMessageFunction = useCallback((message_received) => {
        setMessage(message_received);
    }, [setMessage])

    useEffect(() => {
        if (socket == null) return

        socket.on('send-message', setMessageFunction)

        return () => {
            socket.off('send-message')
        }

    }, [socket, setMessageFunction, props.session])

    useEffect(() => {
        props.modifyMessage(message);
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoConsoleMessage;
