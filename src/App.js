import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import TableSelection from './homepage/TableSelection';
import './App.css';
import { createTheme, ThemeProvider } from '@mui/material/styles'; // MUI에서 필요한 import 추가
import useMediaQuery from '@mui/material/useMediaQuery'; // MUI에서 필요한 import 추가

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [showSearchResult, setShowSearchResult] = useState(false);

  // MUI 테마 설정 및 브레이크포인트 정의
  const theme = createTheme({
    breakpoints: {
      values: {
        xs: 0, // 기본값: 0px 이상
        sm: 600, // 600px 이상
        md: 960, // 960px 이상
        lg: 1280, // 1280px 이상
        xl: 1920, // 1920px 이상
      },
    },
    // 다른 테마 설정...
  });

  return (
    <ThemeProvider theme={theme}> {/* MUI 테마 적용 */}
      <Router>
        <>
          <hr />
          <Link to="/">
            <div className="NineOzImg">
              <img src="http://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" alt="9oz" />
            </div>
          </Link>
          <hr />
          <div className="app-container">
            <Routes>
              <Route path="/" element={<TableSelection />} />
            </Routes>
          </div>
        </>
      </Router>
    </ThemeProvider>
  );
}

export default App;
