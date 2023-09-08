import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import Styles from './NextPage.module.css'
import axios from 'axios';

const NextPage = () => {
    const location = useLocation();  // useLocation을 사용하여 location을 가져옵니다.
    const searchParams = new URLSearchParams(location.search);  // 쿼리 매개변수를 파싱합니다.
    const itemProductCode = searchParams.get('infoProductCode');  // 쿼리 매개변수에서 infoProductCode를 가져옵니다.

    const [productDetails, setProductDetails] = useState(null);

    useEffect(() => {
        const fetchProductDetails = async () => {
            const productcodeURL = `http://10.125.121.170:8080/product/list/${itemProductCode}`;

            try {
                const response = await axios.get(productcodeURL); // await 키워드를 사용하여 비동기 응답을 기다립니다.
                const productDetailsData = response.data[0]; // 응답 데이터는 response.data에 있습니다.
                setProductDetails(productDetailsData);
            } catch (error) {
                console.error('상품 세부 정보를 불러오는데 실패했습니다.', error);
            }
        };

        // 컴포넌트가 마운트될 때 제품 세부 정보를 가져오도록 합니다.
        fetchProductDetails();
    }, [itemProductCode]);

    return (
        <div>
            {productDetails ? (
                <>
                    <img
                        src={`http://10.125.121.170:8080/images/${productDetails.imagePath}`}
                        alt='나인오즈 이미지'
                        onError={(e) => { e.target.src = process.env.PUBLIC_URL + '/none.png'; }}
                        className={Styles.nineozimg}
                    />
                    <p>상품명: {productDetails.productName}</p>
                    <p>상품코드: {productDetails.productCode}</p>
                    <p>판매가격: {productDetails.salePrice}원</p>

                    <Link to="/"><Button>뒤로 가기</Button></Link>
                </>
            ) : (
                <p>상품 정보 불러오는 중...</p>
            )}
        </div>
    );
};

export default NextPage;
