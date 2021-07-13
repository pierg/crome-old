import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoEnvironment(props) {

    const socket = useSocket()

    const [environment, setEnvironment] = useState("");


    const setEnvironmentFunction = useCallback((environment_received) => {
        setEnvironment(environment_received);
    }, [setEnvironment])


    useEffect(() => {
        if (socket == null) return

        socket.emit('get-environment')
        socket.on('receive-environment', setEnvironmentFunction)

        return () => socket.off('receive-environment')
    }, [socket, setEnvironmentFunction])

    useEffect(() => {
        props.modifyEnvironment(environment);
    }, [environment])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoEnvironment;