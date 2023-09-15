import React, { useState } from "react";
import Button from '@mui/material/Button';
import axios from 'axios';

const CrawlButton = () => {
    const [isLoading, setIsLoading] = useState(false);

    const handleCrawl = () => {
        setIsLoading(true);

        // localStorage에서 토큰 가져오기
        const token = localStorage.getItem('accesstoken');

        const config = {
            headers: {
                Authorization: `Bearer ${token}`
            }
        };

        axios.post("http://10.125.121.170:8080/crawl", null, config)
            .then(() => {
                setIsLoading(false);
                console.log('Crawl 버튼을 눌렀습니다.');
            })
            .catch(error => {
                setIsLoading(false);
                console.error('Crawl 중 오류 발생:', error);
            });
    };

    return (
        <>
            <Button onClick={handleCrawl} style={{ border: "1px solid #000", color: "black" }}>
                Crawl
            </Button>
            {isLoading && <p>크롤링 중입니다...</p>}
        </>
    )
}

export default CrawlButton;
