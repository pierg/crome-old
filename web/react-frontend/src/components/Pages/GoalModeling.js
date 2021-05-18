import React from 'react';
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../assets/styles/tailwind.css";


export default class GoalModeling extends React.Component {

    state = {
        numChildren: 0
    }

    handleClick = () => {
        document.getElementById("container").innerHTML += "<div class=\"w-full lg:w-6/12 xl:w-3/12 px-4 text-blueGray-700 rounded border border-solid border-blueGray-100\">Test</div>";
    };

    render() {
        const children = [];

        for (let i = 0; i < this.state.numChildren; i += 1) {
            children.push(<ChildComponent key={i} number={i} />);
        }
        return (
            <ParentComponent addChild={this.onAddChild}>
                {children}
            </ParentComponent>
        );
    }

    onAddChild = () => {
        this.setState({
            numChildren: this.state.numChildren + 1
        });
    }
}

const ParentComponent = props => (
    <section className="mt- md:mt-40 pt-20 relative">
        <div className="px-4 md:px-10 mx-auto w-full">
            <div>
                {/* Card stats */}
                <div className="flex flex-wrap justify-center" id={"container"}>
                    {props.children}
                    <div className="w-full lg:w-6/12 xl:w-3/12 m-4 px-4 bg-lightBlue-600 text-blueGray-700 rounded border border-solid border-blueGray-100">
                        <a href="#" onClick={props.addChild}>Add</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
);

const ChildComponent = props => <div className="w-full lg:w-6/12 xl:w-3/12 m-4 px-4 text-blueGray-700 rounded border border-solid border-blueGray-100">{"I am child " + props.number}</div>;




/*
<div className="container px-4 mx-auto pt-24 ">
                    <div className="flex flex-wrap">
                        <div className="w-full px-4 flex-1"/>
                        <div className="w- px-12 pt-20  flex-1 rounded border border-solid border-blueGray-100">
                            Environment div
                        </div>
                        <div className="w-full px-4 flex-1"/>
                    </div>
                </div>
 */

