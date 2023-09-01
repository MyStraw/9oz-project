import React, { useState } from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import { useNavigate } from 'react-router-dom'; // useNavigate 훅을 불러옵니다.

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '700px',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '700px',
    [theme.breakpoints.up('sm')]: {
      width: '25ch',
      '&:focus': {
        width: '35ch',
      },
    },
  },
}));

export default function SearchAppBar() {
  const [searchQuery, setSearchQuery] = useState(''); // 검색어 상태 추가
  const [searchBy, setSearchBy] = useState('product_code'); // 검색 방법 상태 추가
  const navigate = useNavigate(); // useNavigate 훅을 사용하여 경로 변경 함수를 가져옵니다.

  const handleSearch = () => {
    if (searchQuery.trim() === '') {
      return;
    }

    // 여기에서 검색 방법에 따라 다른 경로로 이동합니다.
    const apiUrl =
      searchBy === 'product_code'
        ? `?product_code=${searchQuery}`
        : `?product_name=${searchQuery}`;

    // 검색 결과 데이터를 전달하면서 새로운 경로로 이동합니다.
    navigate(`/search${apiUrl}`);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton size="large" edge="start" color="inherit" aria-label="open drawer" sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <Search>
            <StyledInputBase
              placeholder="상품명, 상품코드 입력"
              inputProps={{ 'aria-label': 'search' }}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSearch();
                }
              }}
            />
            <IconButton onClick={handleSearch} aria-label="search" color="inherit">
              <SearchIcon />
            </IconButton>
          </Search>
          <RadioGroup
            row
            aria-labelledby="category-radio-group-label"
            name="category-radio-buttons-group"
            value={searchBy}
            onChange={(e) => setSearchBy(e.target.value)}
          >
            <FormControlLabel value="product_code" control={<Radio color="default" />} label="상품코드" style={{ marginLeft: '10px' }} />
            <FormControlLabel value="product_name" control={<Radio color="default" />} label="상품명" />
          </RadioGroup>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, display: { xs: 'none' } }}>
            NINEONCE
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
