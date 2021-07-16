import React, {useEffect} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketSaveGoals(props) {

    const socket = useSocket()

    useEffect(() => {
        if (socket == null) return
        
        if (props.goals !== null && props.triggerSave && props.projectId !== "simple") {
            props.toggleTrigger(0, false)
            socket.emit('save-goals', {goals : props.goals, session : props.session, projectId : props.projectId})

            socket.on('saving-complete', props.toggleTrigger(1, true))
            return () => socket.off('saving-complete')
        }
        
    }, [socket, props])

    return (<></>);
}

export default SocketSaveGoals;