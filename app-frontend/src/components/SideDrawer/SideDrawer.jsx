import React from "react";

import "./SideDrawer.css";

const sideDrawer = (props) => {
  let drawerClasses = "side-drawer";
  if (props.show) {
    drawerClasses = "side-drawer open";
  }

  return (
    <nav className={drawerClasses}>
      <ul>
        <li>Journey Planner</li>
        <li>Station Information</li>
      </ul>
    </nav>
  );
};

export default sideDrawer;