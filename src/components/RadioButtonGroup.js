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
        case 'skirt':
          return (
            <RadioGroup
              row
              aria-labelledby="item-radio-group-label"
              name="item-radio-buttons-group"
              value={selectedItem}
              onChange={handleItemChange}
            >
              <FormControlLabel value="short-skirt" control={<Radio />} label="치마" />
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
        <FormLabel id="category-radio-group-label"></FormLabel>
        <RadioGroup
          row
          aria-labelledby="category-radio-group-label"
          name="category-radio-buttons-group"
          value={selectedCategory}
          onChange={handleCategoryChange}
        >
          <FormControlLabel value="upper" control={<Radio />} label="상의" />
          <FormControlLabel value="outer" control={<Radio />} label="아우터" />
          <FormControlLabel value="onepice" control={<Radio />} label="원피스" />
          <FormControlLabel value="under" control={<Radio />} label="바지" />
          <FormControlLabel value="skirt" control={<Radio />} label="치마" />
        </RadioGroup>
      </FormControl>
      {renderItems()}
    </div>
  );
}
