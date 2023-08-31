import * as React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AppBar from './homepage/AppBar';
import RadioButtonGroup from './homepage/RadioButtonGroup';
import ImageDetail from './predict/ImageDetail';
import './App.css';

function App() {
  const [selectedCategory, setSelectedCategory] = React.useState('');
  const [selectedSubCategory, setSelectedSubCategory] = React.useState('');

  return (
    <Router>
      <>
        <nav>
          <AppBar />
        </nav>
        <div className="NineOzImg">
          <img src="http://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" alt="9oz" />
        </div>
        <div className="app-container">
          <Routes>
            <Route path="/" element={<> {/* or use just <> */}
              <RadioButtonGroup
                onCategoryChange={setSelectedCategory}
                onSubCategoryChange={setSelectedSubCategory}
              />
            </>} />
            <Route path="/predict/..." element={<ImageDetail />} />
          </Routes>
        </div>
      </>
    </Router>
  );
}

export default App;
