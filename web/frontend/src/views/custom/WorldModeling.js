import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import SocketIoMessage from "../../components/Custom/Examples/SocketIoMessage";
import FetchTime from "../../components/Custom/Examples/FetchTime";
import SocketIoPatterns from "../../components/Custom/Examples/GetPatterns";


function WorldModeling() {

    return (
        <>
            <FetchTime/>
            <SocketIoMessage/>
            <SocketIoPatterns/>
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
