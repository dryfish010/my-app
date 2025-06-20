import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import CameraCapture from './camera';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1 className="text-xl font-bold p-4">📸 Camera App</h1>
        <CameraCapture/>
    </>
  )
}

export default App
