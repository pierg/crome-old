import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import ChildComponent from "../../components/Custom/ChildComponent";
import AddGoal from "../../components/Custom/AddGoal";
import {Modal} from "reactstrap";
import GoalEdit from "../../components/Crome/GoalEdit";
import SocketIoGaols from "../../components/Custom/Examples/GetGoals";
import Button from "../../components/Elements/Button";




export default class GoalModeling extends React.Component {

    state = {
        numChildren: 0,
        modalClassic: false,
        goals: []
    }

    render() {
        const children = [];

        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<ChildComponent key={i} number={i}
                  statTitle={this.state.goals[i].name}
                  statDescription={this.state.goals[i].description}
                  statContext="Context of the goal"
                  statObjectives="Objectives of the goal"
                  statIconName="fas fa-pen-square"
                  statSecondIconName="fas fa-trash-alt"
                  statIconColor="bg-lightBlue-600"
                  modify={this.setModalClassic} />);
        }
        return (
            <>
                <Button onClick={this.displayGoals}>Console Log Goals</Button>
                <SocketIoGaols goals={this.getGoals} />
                <ParentComponent addChild={this.onAddChild}>
                    {children}
                </ParentComponent>
                <Modal
                    isOpen={this.state.modalClassic}
                    toggle={() => this.setModalClassic(false)}>
                    <GoalEdit
                        close={() => this.setModalClassic(false)}/>
                </Modal>
            </>
        );
    }

    onAddChild = () => {
        this.setState({
            numChildren: this.state.numChildren + 1
        })
    }

    setModalClassic = (bool) => {
        this.setState({
            modalClassic: bool
        })
    }

    getGoals = (list) => {
        for (let i=0; i<list.length; i++) {
            let tmpArray = this.state.goals
            tmpArray.push(JSON.parse(list[i]))
            this.setState({
                goals: tmpArray,
                //goals: [...this.state.goals, JSON.parse(list[i])]
            })
        }
        this.setState({
            numChildren: list.length
        })
    }

    displayGoals = () => {
        console.log(this.state.goals)
    }
}

const ParentComponent = props => (
    <section className="md:mt-2 pt-20 relative">
        <div className="px-4 md:px-10 mx-auto w-full">
            <div>
                {/* Card stats */}
                <div className="flex justify-center">
                    <div onClick={props.addChild} className="w-full lg:w-6/12 xl:w-3/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-lightBlue-600 rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out">
                        <AddGoal
                            statText="Add a Goal"
                            statIconName="fas fa-plus-square"
                            statIconColor="text-lightBlue-700"
                        /></div></div>
                <div className="flex flex-wrap justify-center">
                    {/*<div onClick={props.addChild} className="w-full lg:w-6/12 xl:w-3/12 m-4 px-4 bg-lightBlue-600 text-blueGray-700 rounded border border-solid border-blueGray-100">*/}
                    {props.children}
                    {/*}</div>*/}
                </div>
            </div>
        </div>
    </section>
);
