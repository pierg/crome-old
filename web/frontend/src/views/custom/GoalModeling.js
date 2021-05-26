import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import ChildComponent from "../../components/Custom/ChildComponent";
import AddGoal from "../../components/Custom/AddGoal";
import {Button, Modal, ModalFooter} from "reactstrap";



export default class GoalModeling extends React.Component {



    state = {
        numChildren: 0,
        modalClassic: false
    }

    render() {
        const children = [];

        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<ChildComponent key={i} number={i}
                  statTitle="Goal Name"
                  statDescription="Description of the goal"
                  statContext="Context of the goal"
                  statObjectives="Objectives of the goal"
                  statIconName="fas fa-pen-square"
                  statSecondIconName="fas fa-trash-alt"
                  statIconColor="bg-lightBlue-600" />);
        }
        return (
            <>
                <ParentComponent addChild={this.onAddChild}>
                    {children}
                </ParentComponent>
                <Button
                    color="info"
                    className="mr-1"
                    onClick={() => this.setModalClassic(true)}
                >
                    <i className="now-ui-icons files_single-copy-04"/> Classic
                </Button>
                <Modal
                    isOpen={this.state.modalClassic}
                    toggle={() => this.setModalClassic(false)}
                >
                    <div className="modal-header justify-content-center">
                        <button
                            aria-hidden={true}
                            className="close"
                            onClick={() => this.setModalClassic(false)}
                            type="button"
                        >
                            <i className="now-ui-icons ui-1_simple-remove"/>
                        </button>
                        <h4 className="title title-up">Modal title</h4>
                    </div>
                    <div className="modal-body">
                        <p>
                            Far far away, behind the word mountains, far from the
                            countries Vokalia and Consonantia, there live the blind
                            texts. Separated they live in Bookmarksgrove right at the
                            coast of the Semantics, a large language ocean. A small
                            river named Duden flows by their place and supplies it with
                            the necessary regelialia. It is a paradisematic country, in
                            which roasted parts of sentences fly into your mouth.
                        </p>
                    </div>
                    <ModalFooter>
                        <Button color="default" type="button">
                            Nice Button
                        </Button>
                        <Button color="danger" onClick={() => this.setModalClassic(false)}>
                            Close
                        </Button>
                    </ModalFooter>
                </Modal>
            </>
        );
    }

    onAddChild = () => {
        this.setState({
            numChildren: this.state.numChildren + 1
        });
        this.setModalClassic(true);
    }

    setModalClassic = (bool) => {
        this.setState({
            modalClassic: bool
        });
    }
}

const ParentComponent = props => (
    <section className="mt- md:mt-40 pt-20 relative">
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
