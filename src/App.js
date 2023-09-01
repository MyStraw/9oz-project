import * as React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import AppBar from './homepage/AppBar';
import TableSelection from './homepage/TableSelection';
import SearchResult from './components/SearchResult';
import './App.css';

const App = () => {
  return (
    <Router>
      <>
        <nav>
          <AppBar />
          <Link to="/">
            <div className="NineOzImg">
              <img src="http://9oz.co.kr/web/upload/NNEditor/20220316/a0bb292ad9713fe53012353fa356a960.png" alt="9oz" />
            </div>
          </Link>
        </nav>
        <div className='tablebar'>
          <TableSelection />
        </div>
        <div className="app-container">
          <Routes>
            <Route path="/search/:query" element={<SearchResult />} />
          </Routes>
        </div>
      </>
    </Router>
  );
}

export default App;
