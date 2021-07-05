import React from 'react';
import {Button, ModalFooter} from "reactstrap";
import Input from "../Elements/Input";

function WorldEdit(props) {


    let element = props.element

    //console.log(element)

    function changeParameter(e) {
        switch (e.target.name) {
            case "name": element = e.target.value; break;
            default: break;
        }
        props.edit(element)
    }

    return(
        <>
            <div className="modal-header justify-content-center">
                <button
                    aria-hidden={true}
                    className="close"
                    onClick={props.close}
                    type="button"
                >
                    <i className={props.info.modal.close}/>
                </button>
                <h4 className="title title-up">{props.info.title}</h4>
            </div>
            <div className="modal-body justify-content-center">
                <Input type="text" placeholder="Name" name="name" value={element} onChange={changeParameter}/>
            </div>
            <ModalFooter>
                <Button color={props.info.modal.cancelColor} onClick={props.close}>
                    {props.info.modal.cancelText}
                </Button>
                <Button color={props.info.modal.saveColor} onClick={() => props.save(element)}>
                    {props.info.modal.saveText}
                </Button>
            </ModalFooter>
        </>
    );
}

export default WorldEdit;