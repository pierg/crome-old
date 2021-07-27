import React, {createRef, useEffect} from "react";
import { useScreenshot, createFileName } from "use-react-screenshot";

export default function CustomDownload (props) {
  const myCanvas = createRef()
  const divCanvas = createRef()

    // eslint-disable-next-line no-unused-vars
  const [screenImage, takeScreenShot] = useScreenshot({
    type: "image/jpeg",
    quality: 1.0
  });

   useEffect(() => {
        if ((props.currentRef === null) && myCanvas.current !== null) {
            props.setRef(myCanvas)
        }
    }, [myCanvas]) // eslint-disable-line react-hooks/exhaustive-deps

  const download = (screenImage, { name = "img", extension = "jpg" } = {}) => {
    const a = document.createElement("a");
    a.href = screenImage;
    a.download = createFileName(extension, name);
    a.click();
  };

  const downloadScreenshot = () => takeScreenShot(divCanvas.current).then(download);

  return (
    <div>
      <button onClick={downloadScreenshot}>Download screenshot</button>
      <div ref={divCanvas}><canvas className="shifted-canvas-margin" ref={myCanvas} id='canvas'/></div>
    </div>
  );
};