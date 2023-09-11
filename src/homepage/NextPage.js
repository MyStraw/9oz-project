import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import Styles from './NextPage.module.css';
import axios from 'axios';

const NextPage = (props) => {
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const itemProductCode = searchParams.get('infoProductCode');

    // 데이터를 props.location.state에서 가져오도록 수정합니다.
    const similarItemUrls = (props.location.state && props.location.state.similarItemUrls) || [];
    console.log(props.location);


    const [productDetails, setProductDetails] = useState(null);

    useEffect(() => {
        const fetchProductDetails = async () => {
            const productcodeURL = `http://10.125.121.170:8080/product/list/${itemProductCode}`;

            try {
                const response = await axios.get(productcodeURL);
                const productDetailsData = response.data[0];
                setProductDetails(productDetailsData);
            } catch (error) {
                console.error('상품 세부 정보를 불러오는데 실패했습니다.', error);
            }
        };

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

                    <div>
                        {similarItemUrls.length > 0 ? (
                            similarItemUrls.map((url, index) => (
                                <img
                                    key={index}
                                    src={url}
                                    alt={`상품 이미지`}
                                />
                            ))
                        ) : (
                            <p>유사 상품 정보가 없습니다.</p>
                        )}
                    </div>
                </>
            ) : (
                <p>상품 정보 불러오는 중...</p>
            )}
        </div>
    );
};

export default NextPage;
