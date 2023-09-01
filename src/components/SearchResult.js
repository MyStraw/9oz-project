import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; // react-router-dom의 useNavigate와 useParams 훅을 불러옵니다.

const SearchResult = () => {
  const { query } = useParams(); // URL에서 query 파라미터를 추출합니다.
  const [searchResults, setSearchResults] = useState([]); // 검색 결과를 저장할 상태 변수
  const [loading, setLoading] = useState(true); // 데이터 로딩 상태 변수
  const navigate = useNavigate(); // useNavigate 훅을 사용하여 경로 변경 함수를 가져옵니다.

  useEffect(() => {
    // API 요청을 보내고 검색 결과를 가져옵니다.
    fetch(`http://10.125.121.170:8080/search?query=${query}`)
      .then((response) => response.json())
      .then((data) => {
        // 데이터에서 results 배열을 추출하여 setSearchResults에 설정합니다.
        setSearchResults(data.results); // 검색 결과를 상태에 저장합니다.
        setLoading(false); // 데이터 로딩이 완료되었음을 표시합니다.
        console.log(query);
      })
      .catch((error) => {
        console.error('Error fetching search results:', error);
        setLoading(false); // 데이터 로딩이 실패한 경우에도 완료되었음을 표시합니다.
      });
  }, [query, navigate]);

  // 데이터 로딩 중에는 로딩 메시지를 표시합니다.
  if (loading) {
    return <div>Loading...</div>;
  }

  // 검색 결과를 화면에 표시합니다.
  return (
    <div>
      <h2>Search Results</h2>
      <ul>
        {searchResults && searchResults.map((result) => (
          <li key={result.id}>{result.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default SearchResult;
