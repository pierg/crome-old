import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import SocketIoMessage from "../../components/Custom/Examples/SocketIoMessage";
import FetchTime from "../../components/Custom/Examples/FetchTime";


function WorldModeling() {

    return (
        <>
            <FetchTime/>
            <SocketIoMessage/>
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
