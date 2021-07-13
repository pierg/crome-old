import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoProjects(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(0);


    const setMessageFunction = useCallback((list_of_projects) => {
        setMessage(list_of_projects);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return

        //socket.emit('get-projects', {session: props.session, project: "simple"})
        socket.emit('get-projects', {session: props.session})
        socket.on('receive-projects', setMessageFunction)

        return () => socket.off('receive-projects')
    }, [socket, setMessageFunction, props.session])

    useEffect(() => {
        props.worlds(message)
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps


    return (<></>);
}

export default SocketIoProjects;
