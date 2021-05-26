import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import SocketIoMessage from "../../components/Custom/Examples/SocketIoMessage";
import FetchTime from "../../components/Custom/Examples/FetchTime";
import SocketIoPatterns from "../../components/Custom/Examples/GetPatterns";
import SocketIoGaols from "../../components/Custom/Examples/GetGoals";


function WorldModeling() {

    return (
        <>
            <FetchTime/>
            <SocketIoMessage/>
            <SocketIoPatterns/>
            <SocketIoGaols/>
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
