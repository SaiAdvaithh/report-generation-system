import SignatureCanvas from "react-signature-canvas";
import { useRef } from "react";

export default function SignaturePad({ setSignature }) {

  const sigRef = useRef();

  const saveSignature = () => {
    const data = sigRef.current.toDataURL();
    setSignature(data);
  };

  return (
    <div>
      <SignatureCanvas
        ref={sigRef}
        penColor="black"
        canvasProps={{ width: 400, height: 200 }}
      />

      <button onClick={saveSignature}>
        Save Signature
      </button>
    </div>
  );
}