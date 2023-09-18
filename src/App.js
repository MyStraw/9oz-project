import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import TableSelection from './homepage/TableSelection';
import './App.css';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import ItemInfo from "./homepage/ItemInfo";
import Login from "./login/Login";
import NewMember from "./login/NewMember";
import CrawlButton from "./components/CrawlButton";
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  // eslint-disable-next-line no-unused-vars
  const [parsedToken, setParsedToken] = useState({});

  const parseJWT = (token) => {
    if (!token) {
      console.error("토큰이 없습니다.");
      return null;
    }

    try {
      // 토큰을 점(.)을 기준으로 나누어 페이로드 부분만 추출
      const payload = token.split('.')[1];

      // Base64Url 포맷을 Base64 포맷으로 변환
      const base64 = payload.replace('-', '+').replace('_', '/');

      // Base64 포맷의 페이로드를 디코딩
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));

      return JSON.parse(jsonPayload);
    } catch (e) {
      console.error("토큰 파싱 중 오류 발생:", e);
      return null;
    }
  }


  useEffect(() => {
    // 토큰 정보 가져오기
    const token = localStorage.getItem('accesstoken');
    if (token) {
      const parsedToken = parseJWT(token);
      if (parsedToken) {
        setParsedToken(parsedToken);
      }
    } else {
      // 토큰이 없을 경우에 대한 처리를 여기에 추가
      console.error("토큰이 없습니다.");
    }
  }, []);


  const theme = createTheme({
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

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

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
            {isLoggedIn ? (
              <>
                <CrawlButton />
                <Button onClick={handleLogout} style={{ margin: '0 10px', border: '1px solid #000', color: 'black' }}>Logout</Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button style={{ margin: '0 10px', border: '1px solid #000', color: 'black' }}>Login</Button>
                </Link>
              </>
            )}
          </div>


          <div className="app-container">
            <Routes>
              <Route path="/" element={<TableSelection />} />
              <Route
                path="/item_info"
                element={<ItemInfo />}
                isLoggedIn={isLoggedIn}
              />
              <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
              <Route path="/new-member" element={<NewMember />} />
            </Routes>
          </div>
        </>
      </Router>
    </ThemeProvider>
  );
}

export default App;
