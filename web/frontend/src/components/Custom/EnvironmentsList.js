import React, {useEffect, useCallback, useState} from 'react'
import {useSocket} from "../../contexts/SocketProvider";

function EnvironmentsList(props) {

    const socket = useSocket()


    const [environments, setEnvironments] = useState(0);



    const setEnvironmentsFunction = useCallback(({ data }) => {
        console.log(data)
        setEnvironments(data);
    },)


    useEffect(() => {
        if (socket == null) return

        socket.emit("get-environments");
        socket.on('receive-environments', setEnvironmentsFunction)

        return () => socket.off('receive-environments')
    }, [socket, setEnvironments])


    return(
        <div className="flex-auto p-4 flex flex-col justify-center items-center">
            <div className="flex flex-wrap flex-col">
                <div className="relative w-full pb-2 max-w-full flex-grow flex-1">
                    <span className="font-bold text-xl uppercase text-white">{props.statText}</span>
                </div>
                <div className="relative w-auto flex flex-initial justify-center">
                    <div
                        className={
                            "bg-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full " +
                            props.statIconColor
                        }
                    >
                        {environments}
                        TEST
                        <i className={props.statIconName}/>
                    </div>
                </div>
            </div>
        </div>);
}

export default EnvironmentsList;
