import React, { useEffect, useState } from 'react';
import Chart from 'react-apexcharts';
import Title from '../Title/Title';
import axios from 'axios';
import HostBackend from '../../../main';
import './Chart.css';


function ChartRequest() {

    const [dataPie, setDataPie] = useState({ ignored: 0, accepted: 0, declined: 0 });

    useEffect(() => {
        axios.get(`${HostBackend}analytics/requests/stats`)
            .then(response => {
                setDataPie(response.data);
            })
            .catch(error => {
                console.error("Ошибка при загрузке данных:", error);
                setDataPie({ ignored: 0, accepted: 0, declined: 0 });
            });
    }, []);

    const options = {
        chart: { type: 'pie', height: 300 },
        labels: ['Принятые', 'Непрочитанные', 'Отклонённые'],
        // dataLabels: {
        //     enabled: true,
        //     formatter: function (val, opts) {
        //         return `${opts.w.globals.labels[opts.seriesIndex]}: ${val.toFixed(2)}%`;
        //     },
        // },
        // tooltip: { y: { formatter: val => `${val.toFixed(2)}%` } },
        legend: { position: 'top', horizontalAlign: 'center' },
        colors: ['#00BC00', 'var(--color-grey)', '#c41e3a'],
    };

    const series = [dataPie.accepted || 0, dataPie.ignored || 0, dataPie.declined || 0];

    return (
        <div className='chart'>
            <div className='chart__item'>
                <Title name='Состояние заявок' />
                <p className='chart__description'>
                    Сколько заявок было отклонено/принято?
                </p>
                <Chart options={options} series={series} type="pie" height={300} />
            </div>
        </div>
    );
}

export default ChartRequest;
