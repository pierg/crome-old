import React, {useEffect} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketSaveEnvironment(props) {

    const socket = useSocket()

    useEffect(() => {
        if (socket == null) return
        
        if (props.world !== null) {
            console.log("SaveEnvironment.js : sent to back-end")
            console.log(props.world)
            props.world.environment.session_id = props.session
            socket.emit('save-project', {session: props.session, world: props.world})
        }
        
    }, [socket, props.world, props.session])

    return (<></>);
}

export default SocketSaveEnvironment;
