import React from 'react';
import ReactApexChart from 'react-apexcharts';

const PieChart = () => {
  // ApexCharts options and config
  const chartOptions = {
    series: [52.8, 26.8, 20.4],
    options: {
      chart: {
        type: 'pie',
        height: 420,
        width: '100%',
      },
      colors: ["#F78181", "#F4FA58", "#F7BE81"],
      stroke: {
        colors: ["white"],
        lineCap: "",
      },
      plotOptions: {
        pie: {
          labels: {
            show: true,
          },
          size: "100%",
          dataLabels: {
            offset: -25,
          },
        },
      },
      labels: ["Direct", "Organic search", "Referrals"],
      dataLabels: {
        enabled: true,
        style: {
          fontFamily: "Inter, sans-serif",
        },
      },
      legend: {
        position: "bottom",
        fontFamily: "Inter, sans-serif",
      },
      yaxis: {
        labels: {
          formatter: function (value) {
            return value + "%";
          },
        },
      },
      xaxis: {
        labels: {
          formatter: function (value) {
            return value + "%";
          },
        },
        axisTicks: {
          show: false,
        },
        axisBorder: {
          show: false,
        },
      },
    },
  };

  return (
    <div>
      <ReactApexChart options={chartOptions.options} series={chartOptions.series} type="pie" height={420} />
    </div>
  );
};

export default PieChart;
