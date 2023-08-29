import React, { useState } from 'react';
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

export default function RowRadioButtonsGroup() {
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedItem, setSelectedItem] = useState('');

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    setSelectedItem('');
  };

  const handleItemChange = (event) => {
    setSelectedItem(event.target.value);
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
            <FormControlLabel value="tshirt" control={<Radio />} label="T셔츠" />
            <FormControlLabel value="blouse" control={<Radio />} label="블라우스" />
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
              <FormControlLabel value="tshirt" control={<Radio />} label="원피스" />
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
      default:
        return null;
    }
  };

  return (
    <div>
      <FormControl>
        <FormLabel id="category-radio-group-label">카테고리 선택</FormLabel>
        <RadioGroup
          row
          aria-labelledby="category-radio-group-label"
          name="category-radio-buttons-group"
          value={selectedCategory}
          onChange={handleCategoryChange}
        >
          <FormControlLabel value="upper" control={<Radio />} label="상의" />
          <FormControlLabel value="onepice" control={<Radio />} label="원피스" />
          <FormControlLabel value="under" control={<Radio />} label="하의" />
        </RadioGroup>
      </FormControl>
      {renderItems()}
    </div>
  );
}
