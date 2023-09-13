import React, { useState } from 'react';
import { Container, Paper, Typography, TextField, Button, Link } from '@mui/material';

const NewMember = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (formData.password !== formData.confirmPassword) {
            alert('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
            return;
        }

        // 회원가입 처리 로직을 추가
        // eslint-disable-next-line no-unused-vars
        const { username, password } = formData;

        // API를 사용하여 서버로 회원가입 데이터를 전송
        // 여기에서 API 호출 또는 데이터베이스 쿼리를 수행할 수 있습니다.

        console.log('회원가입 폼 데이터:', formData);
        // TODO: 실제 회원가입 처리 로직을 작성하세요
    };

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} style={{ padding: '30px', marginTop: '70px' }}>
                <Typography variant="h5" align="center" gutterBottom>
                    회원가입
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField label="사용자 이름" variant="outlined" fullWidth margin="normal" name="username" value={formData.username} onChange={handleChange} required />
                    <TextField label="비밀번호" type="password" variant="outlined" fullWidth margin="normal" name="password" value={formData.password} onChange={handleChange} required />
                    <TextField label="비밀번호 확인" type="password" variant="outlined" fullWidth margin="normal" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} required />
                    <Button type="submit" variant="contained" color="primary" style={{ marginTop: '15px' }} fullWidth margin="normal" >
                        회원가입
                    </Button>
                    <Typography align="center" style={{ marginTop: '15px' }}>
                        <Link href="/login" color="primary">
                            Already member? Log in!
                        </Link>
                    </Typography>
                </form>
            </Paper>
        </Container>
    );
};

export default NewMember;
