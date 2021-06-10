import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import "../../assets/styles/custom.css";
import GoalView from "../../components/Custom/GoalView";
import AddGoal from "../../components/Custom/AddGoal";
import {Modal} from "reactstrap";
import GoalEdit from "../../components/Crome/GoalEdit";
import SocketIoGaols from "../../components/Custom/Examples/GetGoals";
import defaultgoal from "_texts/custom/defaultgoal.js";
import goaleditinfo from "_texts/custom/goaleditinfo.js";
import SocketIoPatterns from "../../components/Custom/Examples/GetPatterns";



export default class GoalModeling extends React.Component {

    state = {
        modalClassic: false,
        goals: [],
        editedGoals: [],
        currentGoalIndex: 0,
        numChildren: 0,
        patterns: []
    }

    render() {
        const children = [];
        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<GoalView key={i} number={i}
                                    title={this.state.goals[i].name}
                                    description={this.state.goals[i].description}
                                    context={this.state.goals[i].context}
                                    contract={this.state.goals[i].contract}
                                    patterns={this.state.patterns}
                                    statIconName={this.props.info.goalComponent.editIconName}
                                    statSecondIconName={this.props.info.goalComponent.deleteIconName}
                                    statIconColor={this.props.info.goalComponent.iconColor}
                                    modify={this.setModalClassic}
                                    delete={this.deleteGoal}
            />);
        }
        return (
            <>
                <SocketIoGaols goals={this.getGoals} />
                <SocketIoPatterns patterns={this.getPatterns} />
                <ParentComponent addChild={this.onAddChild}>
                    {children}
                </ParentComponent>
                <Modal
                    isOpen={this.state.modalClassic}
                    toggle={() => this.setModalClassic(false)}
                    className={"custom-modal-dialog sm:c-m-w-70 md:c-m-w-60 lg:c-m-w-50 xl:c-m-w-40"}>
                    <GoalEdit
                        goal={this.state.editedGoals[this.state.currentGoalIndex]}
                        patterns={this.state.patterns}
                        edit={this.editCurrentGoal}
                        save={this.saveCurrentGoal}
                        close={() => this.setModalClassic(false)}
                        {...goaleditinfo}/>
                </Modal>
            </>
        );
    }

    onAddChild = () => {
        let tmpGoals = this.state.goals
        tmpGoals.push(JSON.parse(JSON.stringify(defaultgoal)))

        this.setState({
            goals: tmpGoals,
            editedGoals: tmpGoals,
            numChildren: this.state.numChildren + 1
        })

        this.setModalClassic(true, tmpGoals.length - 1)
    }

    setModalClassic = (bool, key = -1) => {
        this.setState({
            modalClassic: bool,
            editedGoals: this.state.goals
        })
        if (key !== -1) {
            this.setState({
                currentGoalIndex: key
            })
        }
    }

    deleteGoal = (key) => {
        let tmpGoals = this.state.goals
        tmpGoals.splice(key, 1)
        this.setState({
            goals: tmpGoals,
            editedGoals: tmpGoals,
            numChildren: this.state.numChildren - 1
        })
    }

    editCurrentGoal = (newGoal) => {
        this.setState( state => {
            const editedGoals = state.editedGoals.map((item, j) => {
                if (j === this.state.currentGoalIndex) {
                    return newGoal;
                } else {
                    return item;
                }
            });
            return {
                editedGoals,
            };
        });
    }

    saveCurrentGoal = (newGoal) => {
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
        this.setState({
            editedGoals: this.state.goals
        })
        this.setModalClassic(false)
    }

    getGoals = (list) => {
        let tmpArray = this.state.goals
        for (let i=0; i<list.length; i++) {
            tmpArray.push(JSON.parse(list[i]))
        }
        this.setState({
            goals: tmpArray,
            editedGoals: tmpArray,
            numChildren: list.length
        })
    }

    getPatterns = (list) => {
        this.setState({
            patterns: JSON.parse(list)
        })
    }
}

GoalModeling.defaultProps = {
  contract : ""
};

const ParentComponent = props => (
    <section className="mt-5 mt-xl-2 pt-2 relative">
        <div className="px-4 md:px-10 mx-auto w-full">
            <div>
                <div className="flex justify-center">
                    <div onClick={props.addChild} className="w-full lg:w-6/12 xl:w-3/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-lightBlue-600 rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out">
                        <AddGoal
                            statText="Add a Goal"
                            statIconName="fas fa-plus-square"
                            statIconColor="text-lightBlue-700"
                        /></div></div>
                <div className="flex flex-wrap justify-center">
                    {props.children}
                </div>
            </div>
        </div>
    </section>
);
