// React Component 
import React, { useRef, useState } from 'react';


// 開啟相機
const CameraCapture = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [image, setImage] = useState(null);
    navigator.permissions.query({ name: "camera" }).then((result) => {
        console.log(result.state); // "granted", "denied", or "prompt"
    });

  //開啟相機
  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    videoRef.current.play();
  
  };

  //捕捉照片
  const capturePhoto = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    context.drawImage(videoRef.current, 0, 0);
    const imageData = canvas.toDataURL('image/png');
    setImage(imageData);
  };

  //確認相片後傳入後端
  const sendToServer = async () => {
    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image }),
    });

    const blob = await res.blob();
    const objUrl = URL.createObjectURL(blob);

    // 跳轉到 `show.jsx` 並傳遞 `.obj` 資料
    navigate("/show", { state: { objUrl } });
  };

  return (
    <div className="p-4 space-y-4">
      <video ref={videoRef} className="w-full max-w-md" autoPlay muted />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <div className="flex gap-2">
        <button onClick={startCamera} className="btn">Start Camera</button>
        <button onClick={capturePhoto} className="btn">Capture</button>
        <button onClick={sendToServer} className="btn">Send</button>
      </div>
      {image && <img src={image} alt="Captured" className="mt-4 border rounded" />}
    </div>
  );
};

export default CameraCapture;
