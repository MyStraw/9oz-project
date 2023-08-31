import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate

import Styles from './ImageDetail.module.css';

export default function ImageDetail() {
  const { imagePath, productName, productCode, salePrice } = useParams();
  const [prediction, setPrediction] = useState('');
  const navigate = useNavigate(); // Use useNavigate for navigation

  useEffect(() => {
    axios.post(`http://10.125.121.170:8080/predict/${encodeURIComponent(imagePath)}`)
      .then(response => {
        setPrediction(response.data.prediction);
      })
      .catch(error => {
        console.error('Error sending POST request:', error);
      });
  }, [imagePath]);

  return (
    <div className={Styles.container}>
      <div className={Styles.imageContainer}>
        <img src={`http://10.125.121.170:8080/display?imagePath=${encodeURIComponent(imagePath)}`} alt="이미지" />
      </div>
      <div className={Styles.infoContainer}>
        <p>상품명: {productName}</p>
        <p>상품 코드: {productCode}</p>
        <p>판매 가격: {salePrice}</p>
        <p>예측 결과: {prediction}</p>
        <button onClick={() => navigate(-1)}>뒤로 가기</button>
      </div>
    </div>
  );
}
