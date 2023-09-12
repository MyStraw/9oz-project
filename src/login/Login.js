import React from 'react';
import { Container, Paper, Typography, TextField, Button } from '@mui/material';

const Login = () => {
  return (
    <Container maxWidth="sm">
      <Paper elevation={3} style={{ padding: '60px', marginTop: '70px' }}>
        <Typography variant="h5" align="center" gutterBottom>
          로그인
        </Typography>
        <form>
          <TextField label="ID" variant="outlined" fullWidth margin="normal" />
          <TextField label="Password" type="password" variant="outlined" fullWidth margin="normal" />
          <Button variant="contained" color="primary" style={{ marginTop: '15px' }} fullWidth margin="normal">
            로그인
          </Button>
        </form>
      </Paper>
    </Container>
  );
}

export default Login;

