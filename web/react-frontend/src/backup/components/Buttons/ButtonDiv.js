import React from "react";
import {Link} from "react-router-dom";

// components

export default function ButtonDiv({
    divText,
    buttonText,
    icon,
    link
}
) {
  return (
      <>
          <div className="w-full px-12 pt-20 text-center flex-1 rounded border border-solid border-blueGray-100">
              <div><h3 className="text-2xl mb-2 font-light leading-normal">{divText}</h3></div>
              <div className="pt-6">
                  <Link to={link}>
                      <button className="text-lightBlue-600 bg-transparent border border-solid border-lightBlue-600 active:bg-blueGray-50 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-4 ease-linear transition-all duration-150" type="button">
                          <i className={icon}/> {buttonText}</button>
                  </Link>
              </div>
          </div>
      </>
  );
}
