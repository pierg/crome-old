import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import ChildComponent from "../../components/Custom/ChildComponent";
import AddGoal from "../../components/Custom/AddGoal";
import {Modal} from "reactstrap";
import GoalEdit from "../../components/Crome/GoalEdit";
import SocketIoGaols from "../../components/Custom/Examples/GetGoals";
import Button from "../../components/Elements/Button";
import defaultgoal from "_texts/custom/defaultgoal.js";



export default class GoalModeling extends React.Component {

    state = {
        numChildren: 0,
        modalClassic: false,
        goals: [],
        currentGoalIndex: 0
    }

    render() {
        const children = [];

        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<ChildComponent key={i} number={i}
                  title={this.state.goals[i].name}
                  description={this.state.goals[i].description}
                  context={this.state.goals[i].context}
                  assumptions={this.state.goals[i].contract.assumptions}
                  guarantees={this.state.goals[i].contract.guarantees}
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
                        check={this.displayGoals}
                        goal={this.state.goals[this.state.currentGoalIndex]}
                        save={this.setCurrentGoal}
                        close={() => this.setModalClassic(false)}/>
                </Modal>
            </>
        );
    }

    onAddChild = () => {
        //const defaultProps = `${JSON.stringify(...defaultgoal)}`;
        //const defaultProps = `${JSON.stringify(...defaultgoal)}`;
        let tmpArray = this.state.goals
        tmpArray.push(defaultgoal)
        this.setState({
            goals: tmpArray,
            numChildren: this.state.numChildren + 1
        })
    }

    setModalClassic = (bool, key = false) => {
        //console.log("KEY : "+key)
        this.setState({
            modalClassic: bool
        })
        if (key) {
            this.setState({
                currentGoalIndex: key
            })
        }
    }

    setCurrentGoal = (newGoal) => {
        this.setState( state => {
            const goals = state.goals.map((item, j) => {
                if (j === this.state.currentGoalIndex) {
                    return newGoal;
                } else {
                    return item;
                }
            });
            return {
                goals,
            };
        });
        /*console.log("currentGoal : ")
        console.log(this.state.goals)*/
    }

    getGoals = (list) => {
        for (let i=0; i<list.length; i++) {
            let tmpArray = this.state.goals
            tmpArray.push(JSON.parse(list[i]))
            this.setState({
                goals: tmpArray,
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

GoalModeling.defaultProps = {
  contract : ""
};

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
