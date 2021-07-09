import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoEnvironment(props) {

    const socket = useSocket()

    const [environment, setEnvironment] = useState("");


    const setEnvironmentFunction = useCallback((environment_received) => {
        console.log("message_received")
        //console.log(message_received)
        setEnvironment(environment_received);
    }, [setEnvironment])


    useEffect(() => {
        if (socket == null) return

        socket.emit('get-gridworld')
        socket.on('receive-gridwolrd', setEnvironmentFunction)

        return () => socket.off('receive-gridwolrd')
    }, [socket, setEnvironmentFunction])

    useEffect(() => {
        console.log("sending")
        console.log(environment)
        props.modifyEnvironment(environment);
        console.log(environment)


    }, [environment])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoEnvironment;