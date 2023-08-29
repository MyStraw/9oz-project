import React, { useState } from 'react';
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

export default function RowRadioButtonsGroup() {
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedItem, setSelectedItem] = useState('');
  const [itemInfo, setItemInfo] = useState(null);

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setSelectedItem('');
    setItemInfo(null);
  };

  const handleItemChange = (event) => {
    setSelectedItem(event.target.value);

    // 가상의 아이템 데이터에서 아이템 정보 가져오기
    const itemData = {
      tshirt: { name: '티셔츠', imageUrl: 'https://example.com/tshirt.jpg', description: '티셔츠 설명' },
      blouse: { name: '블라우스', imageUrl: 'https://example.com/blouse.jpg', description: '블라우스 설명' },
      // 다른 아이템 정보 추가
    };

    setItemInfo(itemData[event.target.value]);
  };

  const renderItems = () => {
    switch (selectedCategory) {
      case 'upper':
        return (
          <RadioGroup
            row
            aria-labelledby="item-radio-group-label"
            name="item-radio-buttons-group"
            value={selectedItem}
            onChange={handleItemChange}
          >
            <FormControlLabel value="tshirt" control={<Radio />} label="티셔츠" />
            <FormControlLabel value="blouse" control={<Radio />} label="블라우스" />
            {/* 다른 옵션 추가 */}
          </RadioGroup>
        );
      case 'under':
        return (
          <RadioGroup
            row
            aria-labelledby="item-radio-group-label"
            name="item-radio-buttons-group"
            value={selectedItem}
            onChange={handleItemChange}
          >
            <FormControlLabel value="pants" control={<Radio />} label="바지" />
            <FormControlLabel value="shorts" control={<Radio />} label="반바지" />
            {/* 다른 옵션 추가 */}
          </RadioGroup>
        );
      case 'outer':
        return (
          <RadioGroup
            row
            aria-labelledby="item-radio-group-label"
            name="item-radio-buttons-group"
            value={selectedItem}
            onChange={handleItemChange}
          >
            <FormControlLabel value="jacket" control={<Radio />} label="자켓" />
            <FormControlLabel value="coat" control={<Radio />} label="코트" />
            {/* 다른 옵션 추가 */}
          </RadioGroup>
        );
      case 'onepice':
        return (
          <RadioGroup
            row
            aria-labelledby="item-radio-group-label"
            name="item-radio-buttons-group"
            value={selectedItem}
            onChange={handleItemChange}
          >
            <FormControlLabel value="onepiece" control={<Radio />} label="원피스" />
          </RadioGroup>
        );
      default:
        return null;
    }
  };

  return (
    <div>
      <FormControl>
        <FormLabel id="category-radio-group-label"></FormLabel>
        <RadioGroup
          row
          aria-labelledby="category-radio-group-label"
          name="category-radio-buttons-group"
          value={selectedCategory}
          onChange={handleCategoryChange}
        >
          <FormControlLabel value="upper" control={<Radio />} label="상의" />
          <FormControlLabel value="under" control={<Radio />} label="하의" />
          <FormControlLabel value="outer" control={<Radio />} label="아우터" />
          <FormControlLabel value="onepice" control={<Radio />} label="원피스" />
        </RadioGroup>
      </FormControl>
      {renderItems()}

      {itemInfo && (
        <div>
          <p>선택된 아이템: {itemInfo.name}</p>
          <img src={itemInfo.imageUrl} alt={itemInfo.name} />
          <p>{itemInfo.description}</p>
        </div>
      )}
    </div>
  );
}
