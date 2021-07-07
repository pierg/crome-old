import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoProjects(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(0);


    const setMessageFunction = useCallback((list_of_goals) => {
        //list_of_goals.forEach(goal => console.log(goal));
        setMessage(list_of_goals);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return

        socket.emit('get-projects', {session: "default", project: props.session})
        socket.on('receive-projects', setMessageFunction)

        console.log(message)

        return () => socket.off('receive-projects')
    }, [socket, setMessageFunction, props.session, message])


    return (<></>);
}

export default SocketIoProjects;
