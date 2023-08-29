import * as React from 'react';
import AppBar from './homepage/AppBar';
import RadioButton from './homepage/RadioButtonGroup';
import './App.css';
import ShowingImage from './imageshow/ShowingImage';

function App() {
  return (
    <>
      <nav>
        <AppBar />
      </nav>
      <div className="NineOzImg">
        <img src="https://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" />
      </div>
      <div className="app-container">
        <RadioButton />
      </div>
      <div>
        <ShowingImage />
      </div>
    </>
  );
}

export default App;
