import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import axios from 'axios';

const CrawlButton = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [isCompleted, setIsCompleted] = useState(false);
    const [crawlStatus, setCrawlStatus] = useState('');

    const handleCrawl = () => {
        setIsLoading(true);
        setIsCompleted(false);
        setCrawlStatus('');

        const token = localStorage.getItem('accesstoken');

        const config = {
            headers: {
                Authorization: `Bearer ${token}`
            }
        };

        axios.post("http://10.125.121.170:8080/crawl", null, config)
            .then(response => {
                setIsLoading(false);
                setIsCompleted(true);
                console.log('Crawl 버튼을 눌렀습니다.');
                if (response.data.status) {
                    setCrawlStatus(response.data.status);
                }
            })
            .catch(error => {
                setIsLoading(false);
                setIsCompleted(false);
                console.error('Crawl 중 오류 발생:', error);
            });
    };

    useEffect(() => {
        if (isCompleted) {
            const timer = setTimeout(() => {
                setIsCompleted(false);
                setCrawlStatus('');
            }, 5000);

            return () => clearTimeout(timer);
        }
    }, [isCompleted]);

    return (
        <>
            <Button onClick={handleCrawl} style={{ border: "1px solid #000", color: "black" }}>
                Crawl
            </Button>
            {isLoading && <p>크롤링 중입니다...</p>}
            {isCompleted && <p>{setCrawlStatus}</p>}
            {crawlStatus && <p>{crawlStatus}</p>}
        </>
    )
}

export default CrawlButton;
