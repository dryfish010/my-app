import logo from './logo.svg';
import './App.css';
import CameraCapture from './camera';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://localhost:5000"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <h1 className="text-xl font-bold p-4">📸 Camera App</h1>
          <CameraCapture/>
      </header>
    </div>
  );
}

export default App;
