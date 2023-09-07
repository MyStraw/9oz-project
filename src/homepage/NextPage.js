import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TableSelection = (props) => {
    const { item = {} } = props;
    const [productDetails, setProductDetails] = useState(null);

    useEffect(() => {
        const infoProductCode = item.productCode;
        const iteminfoURL = `http://10.125.121.170:8080/product/list/${infoProductCode}`;

        axios.get(iteminfoURL)
            .then((response) => {
                const productDetails = response.data;
                setProductDetails(productDetails);
            })
            .catch((error) => {
                console.error('상품 세부 정보를 불러오는데 실패했습니다.', error);
            });
    }, [item]);

    return (
        <div>
            {productDetails ? (
                <>
                    <p>productName: {productDetails.productName}</p>
                    <p>productCode: {productDetails.productCode}</p>
                    <p>salePrice: {productDetails.salePrice}</p>
                </>
            ) : (
                <p>No product details available.</p>
            )}
        </div>
    );
};

export default TableSelection;
