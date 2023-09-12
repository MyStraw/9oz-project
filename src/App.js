import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import TableSelection from './homepage/TableSelection';
import './App.css';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import ItemInfo from "./homepage/ItemInfo";
import Login from "./login/Login";

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
            <Link to="/login">
              <Button style={{ border: '1px solid #000', color: 'black' }}>Login</Button>
            </Link>
          </div>

          <div className="app-container">
            <Routes>
              <Route path="/" element={<TableSelection />} />
              <Route path="/item_info" element={<ItemInfo />} />
              <Route path="login" element={<Login />} />
            </Routes>
          </div>
        </>
      </Router>
    </ThemeProvider>
  );
}

export default App;
