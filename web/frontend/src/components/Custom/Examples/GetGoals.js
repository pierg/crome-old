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

        socket.emit('get-goals', {session: "default/simple"})
        socket.on('receive-goals', setMessageFunction)

        return () => socket.off('receive-goals')
    }, [socket, setMessageFunction])

    useEffect(() => {
        props.goals(message)
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketIoGaols;
