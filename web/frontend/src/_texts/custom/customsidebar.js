const textProps = {
  brand: {
    text: "NAME",
    image: require("assets/img/brand/tim_60x61.png").default,
    link: {
      href: "#/index",
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
        href: "#/world",
      },
    },
    {
      icon: "fas fa-tv",
      text: "Run CROME",
      link: {
        href: "#/index",
      },
    },
    {
      divider: true,
    },
    {
      title: "Documentation",
    },
    {
      icon: "fas fa-puzzle-piece",
      text: "Components",
      link: {
        href: "#/components",
      },
    },
    {
      icon: "fas fa-file-alt",
      text: "Overview",
      link: {
        href: "#/documentation",
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
