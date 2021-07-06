import React from "react";

export default function Console({text}) {
  const [sidebarShow, setSidebarShow] = React.useState("y-translate-100");

  return (
    <>
      <nav
        className={
          "block py-4 px-6 bottom-0 w-full bg-black shadow-xl right-0 fixed flex-row flex-nowrap xxl:z-10 z-9999 transition-all duration-300 ease-in-out transform " +
          sidebarShow
        }
      >
          <button
              className="flex items-center justify-center cursor-pointer text-blueGray-700 w-6 h-10 border-l-0 border-r border-t border-b border-solid border-blueGray-100 text-xl leading-none bg-white rounded-r border border-solid border-transparent absolute left-1/2 top--10 z-9998"
              onClick={() => {
                  if (sidebarShow === "y-translate-100") {
                      console.log("ferme");
                      setSidebarShow("y-translate-0");
                  } else {
                      console.log("ouvert");
                      setSidebarShow("y-translate-100");
                  }
              }}
        >
          <i className="fas fa-ellipsis-v"/>
        </button>
            <div>
                {text}
            </div>
      </nav>
    </>
  );
}

Console.defaultProps = {

};

Console.propTypes = {

};
