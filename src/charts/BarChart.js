import React, { useEffect, useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import axios from 'axios';

const BarChart = ({ selectedSortValue, selectedSortColumn, selectedCategory, subCategory }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const dataURL = `http://10.125.121.170:8080/product/list?sort=${selectedSortValue}&sortcolumn=${selectedSortColumn}&mainclass=${selectedCategory}&semiclass=${subCategory}`;
    axios
      .get(dataURL)
      .then((response) => {

        const sortedData = response.data.sort((a, b) => b.totalsale - a.totalsale);
        const topTenData = sortedData.slice(0, 10);
        setData(topTenData);
      })
      .catch((error) => {
        console.error('데이터 가져오기 오류:', error);
      });
  }, [selectedSortValue, selectedSortColumn, selectedCategory, subCategory]);

  const chartOptions = {
    series: [
      {
        name: 'Total Sale',
        data: data.map((item) => item.totalsale),
      },
    ],
    options: {
      chart: {
        type: 'bar',
      },
      plotOptions: {
        bar: {
          horizontal: true,
        },
      },
      xaxis: {
        categories: data.map((item) => item.productName),
        labels: {
          style: {
            colors: '#000',
          },
        },
      },
      colors: ["#8A0886"],
    },
  };

  return (
    <div>
      <ReactApexChart options={chartOptions.options} series={chartOptions.series} type="bar" height={420} />
    </div>
  );
};

export default BarChart;
