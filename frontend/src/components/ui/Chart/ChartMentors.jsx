import React, {useState, useEffect} from 'react';
import Title from '../Title/Title';
import './Chart.css';
import axios from 'axios';
import HostBackend from '../../../main';


function ChartMentors() {

    const [dataMentorsBest, setDataMentorsBest] = useState([]);
    
    useEffect(()=>{
        axios.get(`${HostBackend}analytics/mentors/stats`)
        .then(response => {
            setDataMentorsBest(response.data);
        })
    }, []);

    return (
        <div className='chart'>
            <Title name='Самые лучшие менторы по оценке учеников' />
            <table className='chart__table'>
                <thead>
                    <tr className='table__row'>
                        <th className='table__cell'>Имя ментора</th>
                        <th className='table__cell'>Оценка</th>
                        <th className='table__cell'>Количество оценивших</th>
                    </tr>
                </thead>
                <tbody>
                    {dataMentorsBest.map((mentor, index) => (
                        <tr key={index} className='table__row'>
                            <td className='table__cell cell_name'>{mentor.name}</td>
                            <td className='center-text table__cell'>{mentor.value.toFixed(2)}</td>
                            <td className='table__cell table__count'>{mentor.count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ChartMentors;
