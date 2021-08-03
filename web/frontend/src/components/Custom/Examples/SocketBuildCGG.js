import React, {useEffect} from 'react'
import {useSocket} from "../../../contexts/SocketProvider";

function SocketBuildCGG(props) {

    const socket = useSocket()

    useEffect(() => {
        if (socket == null || !props.trigger) return
        
        switch(props.operator.toLowerCase()) {
            case "conjunction": socket.emit('apply-conjunction', {session: props.session, goals: props.goals }); break;
            case "composition": socket.emit('apply-composition', {session: props.session, goals: props.goals }); break;
            case "disjunction": socket.emit('apply-disjunction', {session: props.session, goals: props.goals }); break;
            case "refinement": socket.emit('apply-refinement', {session: props.session, abstract: props.firstGoal, refined: props.secondGoal }); break;
            case "extension": socket.emit('apply-extension', {session: props.session, input: props.firstGoal, library: props.library }); break;
            default: return
        }
        
        socket.on('operation-complete', props.setTrigger(false))
        return () => socket.off('operation-complete')

    }, [socket, props])

    return (<></>);
}

export default SocketBuildCGG;