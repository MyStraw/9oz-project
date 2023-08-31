import React, { useState } from 'react';
import {
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Button
} from '@mui/material';
import Styles from './RadioButtonGroup.module.css';
import { Link } from 'react-router-dom';
import axios from 'axios';

export default function RadioButtonGroup() {
  const [selectedCategory, setSelectedCategory] = useState('top');
  const [selectedSubCategory, setSelectedSubCategory] = useState('tshirt');
  const [itemData, setItemData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDataLoaded, setIsDataLoaded] = useState(false);

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setSelectedSubCategory('');
    setIsDataLoaded(false);
  };

  const handleSubCategoryChange = (subCategory) => {
    setSelectedSubCategory(subCategory);
    setIsDataLoaded(false);
  };


  const handleImageClick = (item) => {
    const requestData = item.image_path;
    axios.defaults.headers.post['Content-Type'] = 'application/json';
    axios.get(`http://10.125.121.170:8080/list/${selectedCategory}/${selectedSubCategory}`)
      .then(response => {
        const { product_name, product_code, sale_price } = response.data;
        console.log("Product Name:", product_name);
        console.log("Product Code:", product_code);
        console.log("Sale Price:", sale_price);

        const postData = {
          image_path: requestData
        };

        axios.post(`http://10.125.121.170:8080/predict`, postData)
          .then(predictionResponse => {
            console.log(predictionResponse);
          })
          .catch(error => {
            console.error('Error sending POST request:', error);
          });
      })
      .catch(error => {
        console.error('Error fetching product info:', error);
      });
  };




  const fetchItemData = () => {
    const dataURL = `http://10.125.121.170:8080/list/${selectedCategory}/${selectedSubCategory}`;

    if (selectedCategory && selectedSubCategory) {
      setIsLoading(true); // 로딩 시작
      fetch(dataURL)
        .then(response => response.json())
        .then(data => {
          setItemData(data);
          setIsDataLoaded(true);
        })
        .catch(error => console.error('Fetch Error:', error))
        .finally(() => setIsLoading(false)); // 로딩 종료
    }
  };


  const renderSubCategories = () => {
    switch (selectedCategory) {
      case 'top':
        return (
          <RadioGroup
            row
            aria-labelledby="sub-category-radio-group-label"
            name="sub-category-radio-buttons-group"
            value={selectedSubCategory}
            onChange={(event) => handleSubCategoryChange(event.target.value)}
          >
            <FormControlLabel value="tshirt" control={<Radio />} label="티셔츠" />
            <FormControlLabel value="tshirtsleeveless" control={<Radio />} label="티셔츠나시" />
            <FormControlLabel value="knit" control={<Radio />} label="니트" />
            <FormControlLabel value="knitsleeveless" control={<Radio />} label="니트나시" />
            <FormControlLabel value="blouse" control={<Radio />} label="블라우스" />
            <FormControlLabel value="blousesleeveless" control={<Radio />} label="블라우스나시" />
            <FormControlLabel value="shirt" control={<Radio />} label="남방" />
            <FormControlLabel value="jumper" control={<Radio />} label="점퍼" />
            <FormControlLabel value="jacket" control={<Radio />} label="자켓" />
          </RadioGroup>
        );
      case 'bottom':
        return (
          <RadioGroup
            row
            aria-labelledby="sub-category-radio-group-label"
            name="sub-category-radio-buttons-group"
            value={selectedSubCategory}
            onChange={(event) => handleSubCategoryChange(event.target.value)}
          >
            <FormControlLabel value="pants" control={<Radio />} label="바지" />
            <FormControlLabel value="denim" control={<Radio />} label="데님" />
            <FormControlLabel value="skirt" control={<Radio />} label="스커트" />
            <FormControlLabel value="leggings" control={<Radio />} label="레깅스" />
          </RadioGroup>
        );
      case 'outer':
        return (
          <RadioGroup
            row
            aria-labelledby="sub-category-radio-group-label"
            name="sub-category-radio-buttons-group"
            value={selectedSubCategory}
            onChange={(event) => handleSubCategoryChange(event.target.value)}
          >

            <FormControlLabel value="jacket" control={<Radio />} label="자켓" />
            <FormControlLabel value="coat" control={<Radio />} label="코트" />
            <FormControlLabel value="onepiece" control={<Radio />} label="원피스" />
          </RadioGroup>
        );
      default:
        return null;
    }
  };


  return (
    <>
      <div className={Styles.category_select}>
        <FormControl>
          <FormLabel id="category-radio-group-label">카테고리 선택</FormLabel>
          <RadioGroup
            row
            aria-labelledby="category-radio-group-label"
            name="category-radio-buttons-group"
            value={selectedCategory}
            onChange={handleCategoryChange}
            className={Styles.radio_group}
          >
            <FormControlLabel value="top" control={<Radio />} label="상의" />
            <FormControlLabel value="bottom" control={<Radio />} label="하의" />
            <FormControlLabel value="outer" control={<Radio />} label="아우터" />
          </RadioGroup>
        </FormControl>
      </div>
      <div>
        {renderSubCategories()}
      </div>
      <Button onClick={fetchItemData}>데이터 가져오기</Button>
      {isDataLoaded &&
        <div className={Styles.imageGroupContainer}>
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            itemData.map((item) => (
              <div key={item.product_code} className={Styles.imageGroupItem}>
                <Link to="#" onClick={() => handleImageClick(item)}>
                  <img
                    src={`http://10.125.121.170:8080/display?imagePath=${encodeURIComponent(item.image_path)}`}
                    alt='나인오즈 이미지'
                    onError={(e) => {
                      e.target.src = process.env.PUBLIC_URL + '/none.png';
                    }}
                    className={Styles.nineozimg}
                  />
                  <p>{item.product_name}</p>
                  <p>{item.product_code}</p>
                  <p>{item.sale_price}</p>
                </Link>
              </div>
            ))
          )}
        </div>
      }
    </>
  );
}
