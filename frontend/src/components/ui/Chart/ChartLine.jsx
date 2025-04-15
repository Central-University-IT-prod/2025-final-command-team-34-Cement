import React from 'react';
import ApexCharts from 'react-apexcharts';
import Title from '../Title/Title';
import './Chart.css';


function ChartBar(props) {

    let mentors = 0;
    let students = 0;
    let mentorsToStudent = 0;
    
    props.data.map((item) => {
        mentors += item.mentors;
        students += item.students;
    });

    mentorsToStudent = (students / mentors).toFixed(2);

    const options = {
        chart: {
            type: 'line',
            height: 300,
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            width: 3,
            curve: 'smooth',
        },
        xaxis: {
            categories: props.data.map(item => item.name),
        },
        tooltip: {
            shared: true,
            intersect: false,
        },
        legend: {
            position: 'top',
            horizontalAlign: 'left',
        },
        colors: ['#8e44ad', '#fff000'],
    };

    const series = [];

    return (
        <div className='chart'>
            <Title name='Количество принятых/отклоненных заявок менторов на популярные технологии' />
            <p className='chart__description'>В среднем, на одного ментора {mentorsToStudent} учеников</p>
            <ApexCharts options={options} series={series} type="line" height={300} />
        </div>
    );
}

export default ChartBar;
