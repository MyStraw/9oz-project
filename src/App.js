import * as React from 'react';
import RadioButton from './components/RadioButtonGroup'
import AppBar from './components/AppBar'
import './App.css';

function App() {
  return (
    <>
      <nav>
        <AppBar />
      </nav>
      <div className="NineOzImg">
        <img src="https://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" alt="9oz image" />
      </div>
      <div className="app-container">
        <RadioButton />
      </div>
    </>
  );
}

export default App;
