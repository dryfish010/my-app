import { useLocation } from "react-router-dom";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { useLoader } from "@react-three/fiber";

const Show = () => {
  const location = useLocation();
  const objUrl = location.state?.objUrl;

  if (!objUrl) return <p>模型載入失敗</p>;

  const obj = useLoader(OBJLoader, objUrl);

  return <primitive object={obj} />;
};

export default Show;