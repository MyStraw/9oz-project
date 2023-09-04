import React, { useEffect, useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import axios from 'axios';

const PieChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get('http://10.125.121.170:8080/list/top/tshirt') // 티셔츠 예시
      .then((response) => {
        // 데이터를 가져와서 상위 5개 항목을 추출
        const sortedData = response.data.sort((a, b) => b.totalsale - a.totalsale);
        const topFiveData = sortedData.slice(0, 5);
        setData(topFiveData);
      })
      .catch((error) => {
        console.error('데이터 가져오기 오류:', error);
      });
  }, []);

  const chartOptions = {
    series: data.map((item) => item.totalsale),
    options: {
      chart: {
        type: 'pie',
        height: 420,
        width: '100%',
      },
      colors: ["#F78181", "#F4FA58", "#F7BE81", "#81F7D8", "#8181F7"],
    },
  };

  return (
    <div>
      <ReactApexChart options={chartOptions.options} series={chartOptions.series} type="pie" height={420} />
    </div>
  );
};

export default PieChart;
