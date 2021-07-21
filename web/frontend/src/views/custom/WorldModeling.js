import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";
import React from "react";
import AddButton from "../../components/Custom/AddButton";
import WorldView from "../../components/Custom/WorldView";
import {Link} from "react-router-dom";
import SocketIoProjects from "../../components/Custom/Examples/GetProjects";
import {Button, Modal, ModalFooter} from "reactstrap";

export default class WorldModeling extends React.Component {

    state = {
        worlds: [],
        info: [],
        selectedWorldIndex: 0,
        selectedWorldToDelete: 0,
        numChildren: 0,
        modalDeletionConfirmation : false,
        deletionConfirmation: false,
        worldSelected: null
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.project !== this.props.project) {
            this.setState({
                worldSelected: this.getIndexOfProjectId(this.props.project)
            }, () => console.log("worldSelected : "+this.state.worldSelected+", with project : "+this.props.project))
        }
    }

    getWorlds = (list) => {
        let worlds = []
        let info = []
        let names = []

        for (let i=0; i<list.length; i++) {
            for (let j=0; j<list[i].length; j++) {
                if (list[i][j]["title"] === "environment"){
                    worlds.push(JSON.parse(list[i][j]["content"]))
                }
                else if (list[i][j]["title"] === "info") {
                    info.push(JSON.parse(list[i][j]["content"]))
                    names.push(JSON.parse(list[i][j]["content"]).name)
                }
            }
        }

        this.props.setListOfWorldNames(names)

        this.setState({
            worlds: worlds,
            info: info,
            numChildren: worlds.length
        })
    }

    selectWorld = (index, eventId) => {
        if (eventId !== "deleteButton" && eventId !== "deleteIcon") {
            this.setState({
                worldSelected: index,
            })
            this.props.setProject(this.state.worlds[index].project_id)
        }
    }

    modifyWorld = (index) => {
        this.props.setWorld({"environment": this.state.worlds[index], "info": this.state.info[index]})
    }

    clearWorld = () => {
        this.props.setWorld(null)
    }

    setModalDeletionConfirmation = (bool, key = null) => {
        if (bool && key !== null) {
            this.setState({
                selectedWorldToDelete: key,
            })
        }
        this.setState({
            modalDeletionConfirmation: bool,
        })
    }

    setDeletionConfirmation = (bool) => {
        this.setState({
            deletionConfirmation: bool,
        })
    }

    deleteWorld = () => {
        /*let tmpWorlds = this.state.worlds
        let tmpInfo = this.state.info
        tmpWorlds.splice(this.state.selectedWorldToDelete, 1)
        tmpInfo.splice(this.state.selectedWorldToDelete, 1)*/
        if (this.state.selectedWorldToDelete < this.state.worldSelected) {
            this.setState({
                worldSelected: this.state.worldSelected - 1
            })
        }
        /*this.setState({
            worlds: tmpWorlds,
            info: tmpInfo,
            numChildren: this.state.numChildren - 1
        })*/
        this.setModalDeletionConfirmation(false)
        this.setDeletionConfirmation(true)
    }

    getIndexOfProjectId(projectId) {
        if (projectId === 0) return null
        for (let i=0; i<this.state.worlds.length; i++) {
            if (this.state.worlds[i].project_id === projectId) {
                return i
            }
        }
        return this.state.worlds.length
    }

    render() {

        const children = [];
        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<WorldView key={i} number={i}
                                    title={this.state.info[i].name}
                                    description={this.state.info[i].description}
                                    statIconName={this.props.info.goalComponent.editIconName}
                                    statSecondIconName={this.props.info.goalComponent.deleteIconName}
                                    statIconColor={this.props.info.goalComponent.iconColor}
                                    selected={this.state.worldSelected === i}
                                    onClick={(e) => this.selectWorld(i, e.target.id)}
                                    modify={this.modifyWorld}
                                    delete={this.setModalDeletionConfirmation}
            />);
        }

        return (
            <>
                <SocketIoProjects session={this.props.id}
                                  worlds={this.getWorlds}
                                  deletionIndex={this.state.selectedWorldToDelete}
                                  deletionConfirmation={this.state.deletionConfirmation}
                                  deletionChanger={this.setDeletionConfirmation}
                                  projectAdded={this.props.projectAdded}/>
                <ParentComponent clearWorld={this.clearWorld}>
                    {children}
                </ParentComponent>
                <Modal
                    isOpen={this.state.modalDeletionConfirmation}
                    toggle={() => this.setModalDeletionConfirmation(false)}
                    className={"custom-modal-dialog sm:c-m-w-70 md:c-m-w-60 lg:c-m-w-50 xl:c-m-w-40"}>
                    <div className="modal-header justify-content-center">
                        <button
                            aria-hidden={true}
                            className="close"
                            onClick={() => this.setModalDeletionConfirmation(false)}
                            type="button"
                        >
                            <i className={this.props.info.modal.close}/>
                        </button>
                        <h4 className="title title-up">{this.props.info.modal.title}</h4>
                    </div>
                    <div className="modal-body justify-content-center text-center">
                        <span>{this.props.info.modal.content}{this.state.info[this.state.selectedWorldToDelete] !== undefined && this.state.info[this.state.selectedWorldToDelete].name}</span>
                    </div>
                    <ModalFooter>
                        <Button color={this.props.info.modal.cancelColor} onClick={() => this.setModalDeletionConfirmation(false)}>
                            {this.props.info.modal.cancelText}
                        </Button>
                        <Button color={this.props.info.modal.confirmColor} onClick={this.deleteWorld}>
                            {this.props.info.modal.confirmText}
                        </Button>
                    </ModalFooter>
                </Modal>
            </>
        );
    }
}

const ParentComponent = props => (
    <section className="mt-5 mt-xl-2 pt-2 relative">
        <div className="px-4 md:px-10 mx-auto w-full">
            <div>
                <div className="flex justify-center">
                    <div className="w-full lg:w-6/12 xl:w-3/12 mt-8 ml-4 mr-4 px-4 relative flex flex-col min-w-0 break-words bg-lightBlue-600 rounded mb-6 xl:mb-0 shadow-lg opacity-1 transform duration-300 transition-all ease-in-out">
                        <Link to="/world" className="hover-no-underline" onClick={props.clearWorld}><AddButton
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
