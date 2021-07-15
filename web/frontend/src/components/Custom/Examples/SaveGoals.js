import React, {useEffect} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketSaveGoals(props) {

    const socket = useSocket()

    useEffect(() => {
        if (socket == null) return
        
        if (props.goals !== null) {

            socket.emit('save-goals', {goals : props.goals, session : props.session, projectId : props.projectId})
        }
        
    }, [socket, props.goals, props.session, props.projectId])

    return (<></>);
}

export default SocketSaveGoals;