import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import TableSelection from './homepage/TableSelection';
import SearchResult from './components/SearchResult';
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [showSearchResult, setShowSearchResult] = useState(false);

  const handleSearch = () => {
    const query = searchQuery;

    if (!query.trim()) {
      return;
    }

    const searchUrl = `http://10.125.121.170:8080/search?query=${encodeURIComponent(query)}`;

    axios.get(searchUrl)
      .then((response) => {
        const data = response.data;
        console.log('검색 결과:', data);

        const products = data.map((item) => ({
          productCode: item.productCode,
          productName: item.productName,
          salePrice: item.salePrice,
          imagePath: item.imagePath,
        }));

        setProducts(products);
        setShowSearchResult(true);
      })
      .catch((error) => {
        console.error('API 요청 오류:', error);
      });
  };


  return (
    <Router>
      <>
      <hr />
        <Link to="/">
          <div className="NineOzImg">
            <img src="http://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" alt="9oz" />
          </div>
        </Link>
        <hr />
        <div className="app-container">
          <Routes>
            <Route path="/" element={<TableSelection />} />
            <Route path="/search-result" element={showSearchResult ? <SearchResult products={products} /> : null} />
          </Routes>
        </div>
      </>
    </Router >
  );
}

export default App;
