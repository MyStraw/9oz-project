import React from 'react';

const SearchResult = ({ products }) => {
  return (
    <div>
      <h2>Search Results</h2>
      <ul>
        {products.map((item) => (
          <li key={item.productCode}>
            <p>상품명: {item.productName}</p>
            <p>상품코드: {item.productCode}</p>
            <p>색상: {item.colorName}</p>
            <p>사이즈: {item.size}</p>
            <p>가격: {item.salePrice}</p>
            <img src={`http://10.125.121.170:8080/display?imagePath=${encodeURIComponent(item.imagePath)}`} alt={`상품 이미지: ${item.productName}`} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchResult;
