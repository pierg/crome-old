import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function GetCGG(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(null);

    const setMessageFunction = useCallback((received_json) => {
        setMessage(received_json.cgg);
    }, [setMessage])


    useEffect(() => {
        if (socket == null || !props.trigger) return

        socket.emit('process-cgg', {session: props.session})

        socket.on('receive-cgg', setMessageFunction)

        return () => socket.off('receive-cgg')
    }, [socket, setMessageFunction, props.trigger, props.session])

    useEffect(() => {
        props.updateCGG(message)
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default GetCGG;
