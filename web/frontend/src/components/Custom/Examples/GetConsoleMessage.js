import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoConsoleMessage(props) {

    const socket = useSocket()

    const [message, setMessage] = useState("");

    const timeBetweenEachCheck = 2000


    const setMessageFunction = useCallback((message_received) => {
        setMessage(message_received);
    }, [setMessage])

    useEffect(() => {
        if (socket == null) return

        let askForMessages = setInterval(function() {
            socket.emit('ask-console-messages', props.session)
            socket.on('receive-message', setMessageFunction)
        }, timeBetweenEachCheck)

        return () => {
            clearInterval(askForMessages)
            socket.off('receive-message')
        }

    }, [socket, setMessageFunction, props.session])

    useEffect(() => {
        props.modifyMessage(message);
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoConsoleMessage;
