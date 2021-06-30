const textProps = {
  errorMsg: {
      gridTooSmall: "The retracted size is too small, clear before decreasing the size",
      wallInsideBlock: "You can't create a wall within a block",
      wallLine: "Select a line or a column where you want to put a wall",
      splitLocations: "You can't have a location that would be split"
  },
  helpMsg: [
      {
          title: "How to create a Location?",
          content: "Click on a first cell, then click on the opposite corner of the location you want. You will need to enter the id of the location you just created to see it appear."
      },
      {
          title: "How to delete a Location?",
          content: "In the list of locations, click on the cross corresponding to the location you want to delete."
      },
      {
          title: "How to create a Wall?",
          content: "Click on a first wall, then click on the opposite side of the wall you want to create."
      },
      {
          title: "How to delete a Wall?",
          content: "Create a new wall on top of the one you want to delete."
      },
  ],
  componentsList: [
      {
          content: [],
          title: "Locations"
      },
      {
          content: [],
          title: "Actions",
          displayAddButton: true
      },
      {
          content: [],
          title: "Sensors",
          displayAddButton: true
      }
  ]
};
export default textProps;