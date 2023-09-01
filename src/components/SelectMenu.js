import React, { useState } from 'react';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import NativeSelect from '@mui/material/NativeSelect';
import styles from './SelectMenu.module.css'; // CSS 파일 임포트

const SelectMenu = () => {
  const [sort, setSort] = useState('판매량순');

  const handleSortChange = (event) => {
    setSort(event.target.value);
  };

  return (
    <FormControl variant="standard" className={styles.formControl}>
      <InputLabel htmlFor="uncontrolled-native">정렬</InputLabel>
      <NativeSelect
        defaultValue="판매량순"
        inputProps={{
          name: 'age',
          id: 'uncontrolled-native',
        }}
        onChange={handleSortChange}
        className={styles.select} // CSS 클래스 적용
      >
        <option value="판매량순">판매량순</option>
        <option value="상품명">상품명</option>
        <option value="낮은가격">낮은가격</option>
        <option value="높은가격">높은가격</option>
      </NativeSelect>
    </FormControl>
  );
};

export default SelectMenu;
