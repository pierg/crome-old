import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketIoGaols(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(0);


    const setMessageFunction = useCallback((list_of_goals) => {
        //list_of_goals.forEach(goal => console.log(goal));
        setMessage(list_of_goals);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return
        let session = props.projectId === "simple" ? "default" : props.session;
        console.log("session " + session + ", projet_id" + props.projectId)
        socket.emit('get-goals', {session: session, project: props.projectId})
        socket.on('receive-goals', setMessageFunction)

        return () => socket.off('receive-goals')
    }, [socket, setMessageFunction, props.projectId, props.session])

    useEffect(() => {
        props.goals(message)
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoGaols;
