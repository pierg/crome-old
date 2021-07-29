import React, {useEffect} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketSaveEnvironment(props) {

    const socket = useSocket()

    function generateProjectId(name) {
        let rand = Math.floor(Math.random() * 900000) + 100000
        return name.replaceAll(" ","").toLowerCase() + "_" + rand
    }

    useEffect(() => {
        if (socket == null) return
        
        if (props.world !== null && props.trigger) {
            props.world.environment.session_id = props.session
            props.world.info.session_id = props.session

            if (props.world.environment.project_id === null) {
                const projectId = generateProjectId(props.world.info.name)
                props.world.environment.project_id = projectId
                props.world.info.project_id = projectId
            }
            else {
                props.world.info.project_id = props.world.environment.project_id
            }

            props.returnProjectId(props.world.environment.project_id)

            socket.emit('save-project', {world: props.world, session: props.session})

            props.setTrigger(false)
        }
        
    }, [socket, props.world, props])

    return (<></>);
}

export default SocketSaveEnvironment;
