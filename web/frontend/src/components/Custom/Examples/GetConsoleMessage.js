import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoConsoleMessage(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(0);


    const setMessageFunction = useCallback((message_received) => {
        //list_of_goals.forEach(goal => console.log(goal));
        setMessage(message_received);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return

        /*socket.emit('get-goals', {session: "default", project: "simple"})*/
        socket.on('receive-message', setMessageFunction)

        return () => socket.off('receive-message')
    }, [socket, setMessageFunction])

    useEffect(() => {
        props.modifyMessage(message);
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoConsoleMessage;
