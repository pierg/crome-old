import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";
import Button from "../../Elements/Button";

function SocketIoGaols(props) {

    const socket = useSocket()

    const [message, setMessage] = useState(0);


    const setMessageFunction = useCallback((list_of_goals) => {
        console.log(list_of_goals)

        list_of_goals.forEach(goal => console.log(goal));

        setMessage(list_of_goals);
    }, [setMessage])


    useEffect(() => {
        if (socket == null) return

        socket.on('receive-goals', setMessageFunction)

        return () => socket.off('receive-goals')
    }, [socket, setMessageFunction])

    useEffect(() => {
        props.goals(message)
    }, [message])  // eslint-disable-line react-hooks/exhaustive-deps

    function sendMessage() {
        socket.emit('get-goals', {session: "default/simple"})
    }

    return (
        <>
            <Button onClick={sendMessage}>Get Goals Default/Simple</Button>
            {/*<h1>Response:</h1>
            <p>{message}</p>*/}
        </>);
}

export default SocketIoGaols;
