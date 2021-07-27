import React, {createRef, useEffect} from "react";
import { useScreenshot, createFileName } from "use-react-screenshot";

export default function CustomDownload (props) {
  const myCanvas = createRef();

  const [image, takeScreenShot] = useScreenshot({
    type: "image/jpeg",
    quality: 1.0
  });
  
   useEffect(() => {
        props.setRef(myCanvas)
    }, [myCanvas]) // eslint-disable-line react-hooks/exhaustive-deps

  const download = (image, { name = "img", extension = "jpg" } = {}) => {
    const a = document.createElement("a");
    a.href = image;
    a.download = createFileName(extension, name);
    a.click();
  };

  const downloadScreenshot = () => takeScreenShot(props.ref.current).then(download);

  return (
    <div>
      <button onClick={downloadScreenshot}>Download screenshot</button>
      <canvas className="shifted-canvas-margin" ref={myCanvas} id='canvas'/>
    </div>
  );
};