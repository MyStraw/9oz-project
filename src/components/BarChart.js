import React, { useEffect, useState } from 'react';
import ReactApexChart from 'react-apexcharts';
import axios from 'axios';

const BarChart = ({ selectedSortValue, selectedSortColumn, selectedCategory, subCategory, selectedSubCategory, onProductSelect }) => {
  const [data, setData] = useState([]);
  const [showChart, setShowChart] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  function randomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
  // 색상의 명도(lightness)를 반환하는 함수
  function getLightness(hexColor) {
    const r = parseInt(hexColor.slice(1, 3), 16);
    const g = parseInt(hexColor.slice(3, 5), 16);
    const b = parseInt(hexColor.slice(5, 7), 16);

    // 명도 계산 (0-255 범위)
    return (0.299 * r + 0.587 * g + 0.114 * b);
  }


  // 텍스트 색상을 동적으로 선택하는 함수
  function getTextColor(hexColor) {
    const lightness = getLightness(hexColor);
    // 명도가 128 이상이면 검은색, 그렇지 않으면 흰색 반환
    return lightness >= 128 ? '#000' : '#fff';
  }

  // 색상 예시
  const backgroundColor = '#FFFFFF'; // 색상 변경 가능
  const textColor = getTextColor(backgroundColor);

  // 텍스트 요소에 스타일 적용
  <p style={{ color: textColor }}>텍스트 내용</p>


  useEffect(() => {
    const dataURL = `http://localhost:8080/product/list?sort=${selectedSortValue}&sortcolumn=${selectedSortColumn}&mainclass=${selectedCategory}&semiclass=${subCategory}`;
    axios
      .get(dataURL)
      .then((response) => {
        const sortedData = response.data.sort((a, b) => b.totalsale - a.totalsale);
        const topTenData = sortedData.slice(0, 10);

        /* 카테고리별 랜덤 색상 생성 및 추가 **/
        const coloredData = topTenData.map((item) => ({
          ...item,
          color: randomColor(),
        }));

        setData(coloredData);

        if (coloredData.length > 0) {
          setShowChart(true);
        } else {
          setShowChart(false);
        }
      })
      .catch((error) => {
        console.error('데이터 가져오기 오류:', error);
      });
  }, [selectedSortValue, selectedSortColumn, selectedCategory, subCategory]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const initialDataURL = `http://localhost:8080/product/list?sort=${selectedSortValue}&sortcolumn=${selectedSortColumn}&mainclass=${selectedCategory}&semiclass=${subCategory}`;
        const response = await axios.get(initialDataURL);

        const sortedData = response.data.sort((a, b) => b.totalsale - a.totalsale);
        const topTenData = sortedData.slice(0, 10);

        // 카테고리별 랜덤 색상 생성 및 추가
        const coloredData = topTenData.map((item) => ({
          ...item,
          color: randomColor(),
        }));

        setData(coloredData);
        setIsLoading(false);
        setShowChart(true);
      } catch (error) {
        console.error('데이터 가져오기 오류:', error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);


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
          dataLabels: {
            position: 'center',
            style: {
              colors: textColor,
            },
          },
        },
      },
      xaxis: {
        categories: data.map((item) => item.productName),
        labels: {
          style: {
            colors: '#000',
            fontSize: '18px',
          },
        },
      },
      yaxis: {
        labels: {
          style: {
            colors: '#000',
            fontSize: '15px'
          },
        },
      },
      colors: data.map((item) => item.color),
      tooltip: {
        enabled: true,
        y: {
          formatter: function (val) {
            return val + ' 판매량';
          },
        },
      },
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 800,
        animateGradually: {
          enabled: true,
          delay: 150,
        },
        dynamicAnimation: {
          enabled: true,
          speed: 350,
        },
      },
    },
  };








  // 각 항목의 텍스트 색상을 계산하고 설정
  const textColors = chartOptions.options.xaxis.categories.map((category, index) => {
    const item = data[index];
    const textColor = getTextColor(item.color);
    return textColor;
  });

  chartOptions.options.xaxis.labels.style.colors = textColors;

  const handleBarClick = (event, chartContext, config) => {
    const selectedProductName = chartOptions.options.xaxis.categories[config.dataPointIndex];
    onProductSelect(selectedProductName);
  };


  return (
    <>
      <div>
        {isLoading ? (
          <p>로딩중</p>
        ) : showChart ? (
          <ReactApexChart options={chartOptions.options} series={chartOptions.series} type="bar" height={350} events={{ dataPointSelection: handleBarClick }} />
        ) : (
          <p>카테고리를 선택해주세요.</p>
        )}
        <p style={{ color: textColor }}></p>
      </div>
    </>
  );
};

export default BarChart;
