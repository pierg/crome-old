import React, {useCallback, useEffect, useState} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketSaveGoals(props) {

    const socket = useSocket()
    
    const [id, setId] = useState(0);
    
    const setIdFunction = useCallback((project_id) => {
        setId(project_id);
    }, [setId])

    useEffect(() => {
        if (socket == null) return
        
        if (props.goals !== null && props.triggerSave) {
            props.toggleTrigger(0, false)
            socket.emit('save-goals', {goals : props.goals, session : props.session, projectId : props.projectId})

            if (props.projectId === "simple") {
                socket.on('saving-simple', setIdFunction)
                return () => socket.off('saving-simple-complete')
            }
            else {
                socket.on('saving-complete', props.toggleTrigger(1, true))
                return () => socket.off('saving-complete')
            }
        }
        
    }, [socket, props, setIdFunction])
    
    useEffect(() => {
        props.switchWorld(id)
    }, [id])  // eslint-disable-line react-hooks/exhaustive-deps

    return (<></>);
}

export default SocketSaveGoals;