import React from 'react';
import {Button, ModalFooter} from "reactstrap";

function GoalEdit(props) {

    return(
        <>
            <div className="modal-header justify-content-center">
                <button
                    aria-hidden={true}
                    className="close"
                    onClick={props.close}
                    type="button"
                >
                    <i className="now-ui-icons ui-1_simple-remove"/>
                </button>
                <h4 className="title title-up">Edit a Goal</h4>
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
                <Button color="danger" onClick={props.close}>
                    Close
                </Button>
            </ModalFooter>
        </>
    );
}

export default GoalEdit;