const textProps = {
  brand: {
    text: "NAME",
    image: require("assets/img/brand/tim_60x61.png").default,
    link: {
      href: "#/custom-d",
    },
  },
  activeColor: "lightBlue",
  items: [
    {
      divider: true,
    },
    {
      title: "CROME",
    },
      {
      icon: "fas fa-tools",
      text: "Environment Builder",
      link: {
        href: "#/gridworld",
      },
    },
      {
      icon: "fas fa-tv",
      text: "Run CROME",
      active: true,
      link: {
        href: "#/components",
      },
    },
    {
      divider: true,
    },
    {
      title: "LTL Tools",
    },
    {
      icon: "fas fa-map-marked",
      text: "Check Fomulae",
      link: {
        href: "#ltlformulae",
      },
    },
    {
      icon: "fas fa-fingerprint",
      text: "Synthesis Tool",
      link: {
        href: "#ltlsynthesis",
      },
    },
  ],
};
export default textProps;
