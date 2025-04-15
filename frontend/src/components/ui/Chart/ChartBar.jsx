import React, { useState, useEffect, useRef } from 'react';
import ApexCharts from 'react-apexcharts';
import Title from '../Title/Title';
import axios from 'axios';
import HostBackend from '../../../main';
import './Chart.css';

function ChartBar(props) {
    const [dataBar, setDataBar] = useState([]);
    const [theme, setTheme] = useState('dark');
    const wrapperRef = useRef(null); // Ссылка на элемент .wrapper

    // Функция для определения текущей темы
    const getCurrentTheme = () => {
        return document.querySelector('.wrapper').classList.contains('light-theme') ? 'light' : 'dark';
    };

    // Загрузка данных и начальная установка темы
    useEffect(() => {
        axios.get(`${HostBackend}analytics/mentors/tags`)
            .then(response => {
                setDataBar(response.data);
                setTheme(getCurrentTheme()); // Установка начальной темы
            });
    }, []);

    // Отслеживание изменений темы
    useEffect(() => {
        const wrapperElement = document.querySelector('.wrapper');

        // Создаем MutationObserver для отслеживания изменений класса
        const observer = new MutationObserver((mutationsList) => {
            for (let mutation of mutationsList) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    setTheme(getCurrentTheme()); // Обновляем тему при изменении класса
                }
            }
        });

        // Начинаем наблюдение за изменениями класса
        if (wrapperElement) {
            observer.observe(wrapperElement, {
                attributes: true, // Отслеживаем изменения атрибутов
            });
        }

        // Очистка observer при размонтировании компонента
        return () => {
            if (wrapperElement) {
                observer.disconnect();
            }
        };
    }, []);

    // Подсчет общего количества менторов
    let mentors = 0;
    dataBar.forEach((item) => {
        mentors += item.mentors;
    });

    // Настройки диаграммы
    const options = {
        chart: {
            type: 'bar',
            height: 300,
            background: 'transparent', // Прозрачный фон
            foreColor: theme === 'dark' ? '#fff' : '#000', // Цвет текста в зависимости от темы
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '50%',
                endingShape: 'rounded',
            }
        },
        dataLabels: {
            enabled: false,
            style: {
                colors: [theme === 'dark' ? '#fff' : '#000'], // Цвет текста для меток данных
            }
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: dataBar.map(item => item.name),
            labels: {
                style: {
                    colors: theme === 'dark' ? '#fff' : '#000', // Цвет текста для оси X
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: theme === 'dark' ? '#fff' : '#000', // Цвет текста для оси Y
                }
            }
        },
        tooltip: {
            shared: true,
            intersect: false,
            theme: theme, // Тема подсказок
        },
        legend: {
            position: 'top',
            horizontalAlign: 'left',
            labels: {
                colors: theme === 'dark' ? '#fff' : '#000', // Цвет текста для легенды
            }
        },
        grid: {
            borderColor: theme === 'dark' ? '#444' : '#e0e0e0', // Цвет линий сетки
        },
        colors: ['#00BC00'], // Цвет столбцов
    };

    const series = [
        {
            name: 'Менторы',
            data: dataBar.map(item => item.mentors),
        }
    ];

    return (
        <div className='chart'>
            <Title name='Количество менторов по популярным тегам' />
            <p className='chart__description'>
                {mentors} - столько менторов наставляют по популярным тегам
            </p>
            <ApexCharts options={options} series={series} type="bar" height={300} />
        </div>
    );
}

export default ChartBar;