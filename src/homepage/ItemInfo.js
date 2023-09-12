import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import Styles from './NextPage.module.css';
import axios from 'axios';

const ItemInfo = (props) => {
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const itemProductCode = searchParams.get('infoProductCode');

    const [productDetails, setProductDetails] = useState(null);
    const [similarItemUrls, setSimilarItemUrls] = useState([]); // similarItemUrls를 state로 관리

    useEffect(() => {
        const fetchProductDetails = async () => {
            const productcodeURL = `http://10.125.121.170:8080/product/list/${itemProductCode}`;

            try {
                const response = await axios.get(productcodeURL);
                const productDetailsData = response.data[0];
                setProductDetails(productDetailsData);

                // 이 부분에서 similarItemUrls를 설정
                postSimilarImage(productDetailsData); // postSimilarImage 함수를 호출하여 데이터를 가져옵니다.
            } catch (error) {
                console.error('상품 세부 정보를 불러오는데 실패했습니다.', error);
            }
        };

        fetchProductDetails();
    }, [itemProductCode]);

    const postSimilarImage = (item) => {
        const baseImagePath = "C:\\9ozproject\\9OZ_SALES\\";
        const fullPath = baseImagePath + item.imagePath;
        const mainClass = item.mainclass;

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
                const similarItemUrls = response.data.similar_item_urls;

                setSimilarItemUrls(similarItemUrls); // similarItemUrls 상태를 설정합니다.
            })
            .catch((error) => {
                console.error(error);
            });
    };

    return (
        <div className={Styles.iteminfo_recommand}>
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

                    <div className={Styles.recommandImg}>
                        {similarItemUrls.length > 0 ? (
                            similarItemUrls.map((url, index) => {
                                const fileNameWithExtension  = url.substring(url.lastIndexOf('/') + 1);
                                const fileNameWithoutExtension = fileNameWithExtension.replace(/\.[^/.]+$/, "");
                                return (
                                    <div key={index}>
                                        <img src={url} alt={`추천 이미지`} className={Styles.queenitImg} />
                                        <p className={Styles.queenitImgPtags}>{fileNameWithoutExtension}</p>
                                    </div>
                                );
                            })
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

export default ItemInfo;
