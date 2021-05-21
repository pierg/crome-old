import React, { useState, useEffect } from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import EnvironmentsList from "../../components/Custom/EnvironmentsList";




function WorldModeling() {
    const [currentTime, setCurrentTime] = useState(0);

    useEffect(() => {
        fetch('/time').then(res => res.json()).then(data => {
            setCurrentTime(data.time);
        });
    }, []);

    return (
        <>
        {currentTime}
        <EnvironmentsList/>
        </>
    );
}

export default WorldModeling;



//
// export default class WorldModeling extends React.Component {
//
//     render() {
//
//         return (
//             Time()
//         );
//     }
// }
