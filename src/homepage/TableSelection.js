import React, { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import styled from 'styled-components';
import Box from '@mui/material/Box';
import Styles from './TableSelection.module.css';
import SelectMenu from '../components/SelectMenu'
import TextField from '@mui/material/TextField';
import { Link } from 'react-router-dom';
import Doughnutchart from '../charts/PieChart'
import axios from 'axios';
import { useMediaQuery } from '@mui/material';

const TableSelection = () => {
    const StyledBox = styled(Box)`
        & button {
            m: 1;
            width: 280px;
            height: 60px;
            font-size: 20px;
            &:focus {
                box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.5);
            }
            color: black;
        }
    `;
    const isMobile = useMediaQuery((theme) => theme.breakpoints.down('sm'));

    // 모바일 화면 여부에 따라 버튼 스타일 설정
    const buttonStyle = isMobile
        ? { m: 1, width: '140px', height: '50px', fontSize: '10px', color: 'black' }
        : { m: 1, width: '280px', height: '60px', fontSize: '20px', color: 'black' };

    const [selectedCategory, setSelectedCategory] = useState(null);
    const [selectedSubCategory, setSelectedSubCategory] = useState(null);
    const [itemData, setItemData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isDataLoaded, setIsDataLoaded] = useState(false);
    const [searchQuery, setSearchQuery] = useState(''); // 추가: 검색어 상태

    const handleCategorySelect = (category) => {
        setSelectedCategory(category);
        setSelectedSubCategory(null);
    };

    const handleSubCategorySelect = (subCategory) => {
        setSelectedSubCategory(subCategory);
        setItemData([]);
        setIsDataLoaded(false);

        const dataURL = `http://10.125.121.170:8080/list/${selectedCategory}/${subCategory}`;

        if (selectedCategory && subCategory) {
            setIsLoading(true);
            fetch(dataURL)
                .then(response => response.json())
                .then(data => {
                    setItemData(data);
                    setIsDataLoaded(true);
                })
                .catch(error => console.error('Fetch Error:', error))
                .finally(() => setIsLoading(false));
        }
    };

    const handleImageClick = (item) => {
        const requestData = {
            image_path: item.image_path,
        };

        axios.get(`http://10.125.121.170:8080/list/${selectedCategory}/${selectedSubCategory}`)
            .then(response => {
                const { productName, productCode, salePrice } = response.data;
                console.log("ProductName:", productName);
                console.log("ProductCode:", productCode);
                console.log("SalePrice:", salePrice);

                axios.post(`http://10.125.121.170:8080/predict`, (requestData))
                    .then(predictionResponse => {
                        console.log(predictionResponse);
                    })
                    .catch(error => {
                        console.error(error);
                    });
            })
            .catch(error => {
                console.error('Error fetching product info:', error);
            });
    };



    const handleSearch = () => {
        if (!searchQuery.trim()) {
            return;
        }

        const searchUrl = `http://10.125.121.170:8080/search?query=${encodeURIComponent(searchQuery)}`;

        axios.get(searchUrl)
            .then(response => {
                const data = response.data;
                console.log('검색 결과:', data);

                const products = data.map(item => ({
                    productCode: item.productCode,
                    productName: item.productName,
                    salePrice: item.salePrice,
                    imagePath: item.imagePath,
                }));

                setItemData(products);
                setIsDataLoaded(true);
            })
            .catch(error => {
                console.error('API 요청 오류:', error);
            });
    };

    useEffect(() => {
        // 검색어가 변경될 때 검색 함수를 호출
        handleSearch();
    }, [searchQuery]);

    const renderCategoryButtons = () => {
        return (
            <StyledBox sx={{ '& button': buttonStyle }}>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('top')}> 상의 </Button>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('bottom')}> 하의 </Button>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('outer')}> 아우터 </Button>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('onepiece')}> 원피스 </Button>
            </StyledBox>
        );
    };

    const renderSubCategories = () => {
        return (
            <div>
                {selectedCategory === 'top' && (
                    <StyledBox sx={{ '& button': buttonStyle }}>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('tshirt')}>티셔츠</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('tshirtsleeveless')}>티셔츠나시</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('knit')}>니트</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('knitsleeveless')}>니트나시</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('blouse')}>블라우스</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('blousesleeveless')}>블라우스나시</Button>
                    </StyledBox>
                )}
                {selectedCategory === 'bottom' && (
                    <StyledBox sx={{ '& button': buttonStyle }}>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('pants')}>바지</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('denim')}>데님</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('skirt')}>스커트</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('leggings')}>레깅스</Button>
                    </StyledBox>
                )}
                {selectedCategory === 'outer' && (
                    <StyledBox sx={{ '& button': buttonStyle }}>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('jacket')}>자켓</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('coat')}>남방</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('jumper')}>점퍼</Button>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('vest')}>베스트(vest)</Button>
                    </StyledBox>
                )}
                {selectedCategory === 'onepiece' && (
                    <StyledBox sx={{ '& button': buttonStyle}}>
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('onepiece')}>원피스</Button>
                    </StyledBox>
                )}
            </div>
        );
    };

    return (
        <>
            <div className={`${Styles.main_input} ${Styles.mobileCenter}`}>
                <div className={Styles.searchContainer}>
                    <TextField id="outlined-basic" label="검색어 입력" variant="outlined" size="small" onChange={(e) => setSearchQuery(e.target.value)} />
                </div>
                <SelectMenu />
            </div>
            <div className={Styles.mainbutton}>
                <div className={Styles.category_select}>
                    {renderCategoryButtons()}
                </div>
                <div className={Styles.category_select}>
                    {renderSubCategories()}
                </div>
                <div>
                    <Doughnutchart />
                </div>
            </div>
            {isDataLoaded && (
                <div className={Styles.imageGroupContainer}>
                    {isLoading ? (
                        <div className={Styles.loadingContainer}>
                            <p>Loading...</p>
                        </div>
                    ) : (
                        itemData.map((item) => (
                            <div key={item.productCode} className={Styles.imageGroupItem}>
                                <Link to="#" onClick={() => handleImageClick(item)}>
                                    <img
                                        src={`http://10.125.121.170:8080/display?imagePath=${encodeURIComponent(item.imagePath)}`}
                                        alt='나인오즈 이미지'
                                        onError={(e) => { e.target.src = process.env.PUBLIC_URL + '/none.png'; }}
                                        className={Styles.nineozimg}
                                    />
                                    <div className={Styles.product_info}>
                                        <p className={Styles.prdname}>제품명: {item.productName}</p>
                                        <p>제품코드: {item.productCode}</p>
                                        <p>가격: {item.salePrice}</p>
                                    </div>
                                </Link>
                            </div>
                        ))
                    )}
                </div>
            )}
        </>
    );
}

export default TableSelection;
