import React, { useEffect, useState } from 'react';
import Chart from 'react-apexcharts';
import Title from '../Title/Title';
import axios from 'axios';
import HostBackend from '../../../main';
import './Chart.css';


function ChartPie() {
    const [dataPie, setDataPie] = useState({ students: 0, mentors: 0 });

    useEffect(() => {
        axios.get(`${HostBackend}analytics/count/`)
            .then(response => {
                setDataPie(response.data);
            })
            .catch(error => {
                console.error("Ошибка при загрузке данных:", error);
                setDataPie({ students: 0, mentors: 0 });
            });
    }, []);

    const mentorsToStudent = dataPie.mentors > 0 
        ? (dataPie.students / dataPie.mentors).toFixed(2) 
        : 'Нет данных';

    const options = {
        chart: { type: 'donut', height: 300 },
        labels: ['Ученики', 'Менторы'],
        dataLabels: {
            enabled: true,
            formatter: function (val, opts) {
                return `${opts.w.globals.labels[opts.seriesIndex]}: ${val.toFixed(2)}%`;
            },
        },
        tooltip: { y: { formatter: val => `${val.toFixed(2)}%` } },
        legend: { position: 'top', horizontalAlign: 'center' },
        colors: ['#00BC00', '#c41e3a'],
    };

    const series = [dataPie.students || 0, dataPie.mentors || 0];

    return (
        <div className='chart'>
            <div className='chart__item'>
                <Title name='Отношение учеников к менторам' />
                <p className='chart__description'>
                    В среднем, на одного ментора {mentorsToStudent} учеников
                </p>
                <Chart options={options} series={series} type="donut" height={300} />
            </div>
        </div>
    );
}

export default ChartPie;
