import React from "react";

export default function Console({text, customText}) {
    const [sidebarShow, setSidebarShow] = React.useState("y-translate-100");
    const [logoState, setLogoState] = React.useState("fas fa-chevron-up");

    return (
        <>
            <nav
                className={
                    "block py-4 px-6 bottom-0 w-full bg-blueGray-800 shadow-xl right-0 fixed flex-row flex-nowrap xxl:z-10 z-9999 transition-all duration-300 ease-in-out transform " +
                    sidebarShow
                }
            >
                <button
                    className="flex items-center justify-center cursor-pointer text-blueGray-700 w-10 h-6 border-l-0 border-r border-t border-b border-solid border-blueGray-100 text-xl leading-none bg-white rounded-r border border-solid border-transparent absolute left-1/2 top--10 z-9998"
                    onClick={() => {
                        if (sidebarShow === "y-translate-100") {
                            setSidebarShow("y-translate-0");
                            setLogoState("fas fa-chevron-down");
                        } else {
                            setSidebarShow("y-translate-100");
                            setLogoState("fas fa-chevron-up");
                        }
                    }}
                >
                    <i className={logoState}/>
                </button>
                <div className="text-white">
                    {customText || text}
                </div>
            </nav>
        </>
    );
}

Console.defaultProps = {

};

Console.propTypes = {

};
