import React, { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import styled from 'styled-components';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Styles from './TableSelection.module.css';
import TextField from '@mui/material/TextField';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useMediaQuery } from '@mui/material';
import BarChart from '../charts/BarChart';

const TableSelection = () => {
    const StyledBox = styled(Box)`
        & button {
            m: 1;
            width: 280px;
            height: 60px;
            font-size: 20px;
            &:focus {
                box-shadow: 0 0 0 0.3rem #33FFFF;
            }
            color: black;
        }
    `;


    const isMobile = useMediaQuery((theme) => theme.breakpoints.down('sm'));

    // 모바일 화면 여부에 따라 버튼 스타일 설정
    const buttonStyle = isMobile
        ? { m: 1, width: '140px', height: '50px', fontSize: '10px', color: 'black' }
        : { m: 1, width: '200px', height: '50px', fontSize: '15px', color: 'black' };

    const [selectedCategory, setSelectedCategory] = useState(null);
    const [selectedSubCategory, setSelectedSubCategory] = useState(null);
    const [itemData, setItemData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isDataLoaded, setIsDataLoaded] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedSortValue, setSelectedSortValue] = useState('desc');
    const [selectedSortColumn, setSelectedSortColumn] = useState('totalsale');
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 20;

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = itemData.slice(indexOfFirstItem, indexOfLastItem);


    const handleCategorySelect = (category) => {
        setSelectedCategory(category);
        setSelectedSubCategory(null);
        paginate(1);
    };
    const handleSortChange = (event) => {
        const selectedSortValue = event.target.value;
        const selectedField = event.target.name;

        if (selectedField === 'sort') {
            setSelectedSortValue(selectedSortValue);
        } else if (selectedField === 'sortcolumn') {
            setSelectedSortColumn(selectedSortValue);
        }
    };


    const handleSubCategorySelect = (subCategory) => {
        setSelectedSubCategory(subCategory);
        setItemData([]);
        setIsDataLoaded(false);

        // 여기서 dataURL 생성 시, 파라미터 순서를 올바르게 조정
        const dataURL = `http://10.125.121.170:8080/product/list?sort=${selectedSortValue}&sortcolumn=${selectedSortColumn}&mainclass=${selectedCategory}&semiclass=${subCategory}`;

        if (selectedSortValue !== 'none' && selectedSortColumn !== 'none' && selectedCategory && subCategory) {
            setIsLoading(true);
            axios.get(dataURL)
                .then(response => response.data)
                .then(data => {
                    setItemData(data);
                    setIsDataLoaded(true);
                })
                .catch(error => console.error('Fetch Error:', error))
                .finally(() => setIsLoading(false));
        }
    };
    const navigate = useNavigate();
    const handleImageClick = (item) => {


        const baseImagePath = "C:\\9ozproject\\9OZ_SALES\\";
        const fullPath = baseImagePath + item.imagePath;
        const mainClass = item.mainclass;
        const itemProductCode = item.productCode;

        const requestData = {
            image_path: fullPath,
            mainclass: mainClass
        };

        axios.post('http://10.125.121.170:8080/predict', requestData, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => {
                // 응답 데이터를 확인하여 데이터가 예상대로 들어 있는지 확인합니다.
                console.log(response.data); // 응답 데이터를 콘솔에 출력해 보세요.

                // 유사 상품 URL 배열을 추출합니다.
                const similarItemUrls = response.data.similar_item_urls;
                console.log(similarItemUrls)

                // NextPage 컴포넌트로 넘기기 위해 페이지 이동합니다.
                navigate('/item_info?infoProductCode=' + itemProductCode, { similarItemUrls });
            })
            .catch((error) => {
                console.error(error);
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
        handleSearch();
        // eslint-disable-next-line
    }, [searchQuery]);

    useEffect(() => {
        const initialDataURL = `http://10.125.121.170:8080/product/list?sort=desc&sortcolumn=totalsale`;

        axios.get(initialDataURL)
            .then(response => response.data)
            .then(data => {
                setItemData(data);
                setIsDataLoaded(true);
            })
            .catch(error => console.error('Fetch Error:', error))
            .finally(() => setIsLoading(false));
    }, []);

    const renderCategoryButtons = () => {
        return (
            <StyledBox sx={{ '& button': buttonStyle }}>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('top')}> 상의 </Button>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('bottom')}> 하의 </Button>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('outer')}> 아우터 </Button>
                <Button variant="outlined" size="large" onMouseEnter={() => handleCategorySelect('onepiece')} onClick={() => handleSubCategorySelect('onepiece')}> 원피스 </Button>
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
                        <Button variant="outlined" onClick={() => handleSubCategorySelect('cardigan')}>가디건</Button>
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
            </div>
        );
    };

    const paginate = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    const renderPagination = () => {
        const pageNumbers = Math.ceil(itemData.length / itemsPerPage);

        // 현재 페이지를 기준으로 현재 블록을 계산
        const currentBlock = Math.ceil(currentPage / 10);
        const startPage = (currentBlock - 1) * 10 + 1;
        const endPage = currentBlock * 10;

        return (
            <div className={Styles.pageButton}>
                {currentBlock > 1 && (
                    <Button onClick={() => paginate(startPage - 1)}>{'이전'}</Button>
                )}

                {Array.from({ length: pageNumbers }, (_, index) => {
                    if (index + 1 >= startPage && index + 1 <= endPage) {
                        return (
                            <Button
                                key={index}
                                onClick={() => paginate(index + 1)}
                                className={`${Styles.pageButton} ${currentPage === index + 1 ? Styles.activePage : ''}`}
                            >
                                {index + 1}
                            </Button>

                        );
                    }
                    return null;
                })}

                {currentBlock < Math.ceil(pageNumbers / 10) && (
                    <Button onClick={() => paginate(endPage + 1)}>{'다음'}</Button>
                )}
            </div>
        );
    };




    const renderItems = () => {
        return currentItems.map((item) => (
            <div key={item.id} className={Styles.imageGroupItem}>
                <Link to="/item_info" onClick={() => handleImageClick(item)}>
                    <img
                        src={`http://10.125.121.170:8080/images/${item.imagePath}`}
                        alt='나인오즈 이미지'
                        onError={(e) => { e.target.src = process.env.PUBLIC_URL + '/none.png'; }}
                        className={Styles.nineozimg}
                    />
                </Link>
                <div className={Styles.product_info}>
                    <p className={Styles.prdname}>제품명: {item.productName}</p>
                    <p>제품코드: {item.productCode}</p>
                    <p>가격: {item.salePrice}원(￦)</p>
                </div>
            </div>
        ));
    };



    return (
        <>
            <div className={`${Styles.main_input} ${Styles.mobileCenter}`}>
                <div className={Styles.searchContainer}>
                    <TextField id="outlined-basic" label="검색어 입력" variant="outlined" size="small" onChange={(e) => setSearchQuery(e.target.value)} />
                </div>
                <FormControl variant="outlined" size="small">
                    <Select
                        className="select_sort"
                        onChange={(e) => handleSortChange(e)}
                        defaultValue={'desc'}
                        name="sort"
                    >
                        <MenuItem value="none">선택</MenuItem>
                        <MenuItem value="asc">오름차순</MenuItem>
                        <MenuItem value="desc">내림차순</MenuItem>
                    </Select>
                </FormControl>

                <FormControl variant="outlined" size="small">
                    <Select
                        className="select_sort_ascdesc"
                        onChange={(e) => handleSortChange(e)}
                        defaultValue={'totalsale'}
                        name="sortcolumn"
                    >
                        <MenuItem value="none">선택</MenuItem>
                        <MenuItem value="totalsale">판매량순</MenuItem>
                        <MenuItem value="productName">상품명</MenuItem>
                        <MenuItem value="salePrice">판매가격순</MenuItem>
                    </Select>
                </FormControl>

            </div>
            <div className={Styles.mainbutton}>
                <div className={Styles.category_select}>
                    {renderCategoryButtons()}
                </div>
                <div className={Styles.category_select}>
                    {renderSubCategories()}
                </div>
            </div>
            <div className={`${Styles.barChartContainer}`}>
                <BarChart selectedSortValue={selectedSortValue} selectedSortColumn={selectedSortColumn} selectedCategory={selectedCategory} subCategory={selectedSubCategory} />
            </div>
            {isDataLoaded && (
                <div className={Styles.imageGroupContainer}>
                    {isLoading ? (
                        <p>로딩중</p>
                    ) : (
                        <>
                            {renderItems()}
                            <div className={`${Styles.centered}`}>
                                {renderPagination()}
                            </div>
                        </>
                    )}
                </div>
            )}
        </>
    );
}

export default TableSelection;
