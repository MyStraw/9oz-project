import React, { useState } from 'react';
import { Container, Paper, Typography, TextField, Button } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = ({ setIsLoggedIn }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();


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

    const loginData = {
      username: username,
      password: password,
    };


    const response = await axios.post('http://10.125.121.170:8080/login', loginData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.data.message === '로그인 성공') {
      setIsLoggedIn(true);
      const accessToken = response.headers['authorization'];
      const parsedToken = parseJWT(accessToken);
      if (parsedToken) {
        localStorage.setItem('username', parsedToken.username);
        localStorage.setItem('accesstoken', accessToken);
      }

      navigate("/");
    } else {
      console.error('로그인 실패');
      setError('비밀번호가 틀렸습니다.');
    }
  };


  return (
    <Container maxWidth="sm">
      <Paper elevation={3} style={{ padding: '60px', marginTop: '70px' }}>
        <Typography variant="h5" align="center" gutterBottom>
          로그인
        </Typography>
        <form onSubmit={handleLogin}>
          <TextField label="ID" variant="outlined" fullWidth margin="normal" value={username} onChange={(e) => setUsername(e.target.value)} />
          <TextField label="Password" type="password" variant="outlined" fullWidth margin="normal" value={password} onChange={(e) => setPassword(e.target.value)} />
          <Button type="submit" variant="contained" color="primary" style={{ marginTop: '15px' }} fullWidth margin="normal">
            로그인
          </Button>
        </form>
        <Typography align="center" style={{ marginTop: '15px' }}>
          {error && <Typography variant="body2" color="error">{error}</Typography>}
        </Typography>
      </Paper>
    </Container>
  );
}

export default Login;
