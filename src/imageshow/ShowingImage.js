import React, { useState, useEffect } from 'react';

const ShowingImage = () => {
  const [imageData, setImageData] = useState([]);
  
  // API에서 데이터 가져오기
  useEffect(() => {
    fetch('http://10.125.121.150:8080/9ozclothes/tshirts')
      .then(response => response.json())
      .then(data => setImageData(data)); // 이미지 데이터를 state에 저장
  }, []);

  return (
    <div>
      {imageData.map(item => (
        <div key={item.id}>
          <img src={item.imageURL} alt={`Image ${item.id}`} />
          <p>{item.title}</p>
          <p>{item.description}</p>
          {/* 나머지 정보도 렌더링 */}
        </div>
      ))}
    </div>
  );
};

export default ShowingImage;
