import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import React from "react";
import AddButton from "../../components/Custom/AddButton";
import WorldView from "../../components/Custom/WorldView";
import {Link} from "react-router-dom";
import SocketIoGaols from "../../components/Custom/Examples/GetGoals";
import SocketIoProjects from "../../components/Custom/Examples/GetProjects";


export default class WorldModeling extends React.Component {

    state = {
        worlds: [],
        currentGoalIndex: 0,
        numChildren: 0,
    }

    render() {

        const children = [];
        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<WorldView key={i} number={i}
                                    title={this.state.worlds[i].name}
                                    description={this.state.worlds[i].description}
                                    statIconName={this.props.info.goalComponent.editIconName}
                                    statSecondIconName={this.props.info.goalComponent.deleteIconName}
                                    statIconColor={this.props.info.goalComponent.iconColor}
                                    modify={this.setModalClassic}
                                    delete={this.deleteGoal}
            />);
        }

        return (
            <>
                <SocketIoProjects />
                {/*<SocketIoWorlds worlds={this.getWorlds} />*/}
                <ParentComponent build={this.redirectToBuilding}>
                    {children}
                </ParentComponent>
            </>
        );
    }

    redirectToBuilding = () => {
        console.log("redirection")
    }

}

const ParentComponent = props => (
    <section className="mt-5 mt-xl-2 pt-2 relative">
        <div className="px-4 md:px-10 mx-auto w-full">
            <div>
                <div className="flex justify-center">
                    <div onClick={props.build} className="w-full lg:w-6/12 xl:w-3/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-lightBlue-600 rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out">
                        <Link to="/world" className="hover-no-underline"><AddButton
                            statText="Build your Environment"
                            statIconName="fas fa-plus-square"
                            statIconColor="text-lightBlue-700"
                        /></Link>
                    </div>
                </div>
                <div className="flex flex-wrap justify-center">
                    {props.children}
                </div>
            </div>
        </div>
    </section>
);

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
