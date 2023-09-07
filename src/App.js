import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import TableSelection from './homepage/TableSelection';
import './App.css';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import NextPage from "./homepage/NextPage";

function App() {
  const theme = createTheme({
    //반응형 웹을 위해 기본 breakpoints 값
    breakpoints: {
      values: {
        xs: 0,
        sm: 600,
        md: 960,
        lg: 1280,
        xl: 1920,
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <>
          <hr />
          <a href="/">
            <div className="NineOzImg">
              <img src="http://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" alt="9oz" />
            </div>
          </a>
          <hr />
          <div className="login-button-container">
            <Button>Login</Button> {/* 로그인 버튼 */}
          </div>

          <div className="app-container">
            <Routes>
              <Route path="/" element={<TableSelection />} />
              <Route path="/item_info" element={<NextPage />} />
            </Routes>
          </div>
        </>
      </Router>
    </ThemeProvider>
  );
}

export default App;
