import React from 'react';
import './Home.css';
import Button from '../../ui/Button/Button.jsx';
import Tags from '../../ui/Tags/Tags.jsx';


function Home(props) {

    return (
        <div className='home'>
            <section className="home__buttons">
                <div className="buttons__block">
                    <Button button_data={{
                        title: 'Статистика по тегам',
                        background: '#4D8AA8',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: true,
                        path: 'count_mentors',
                        minWidth: '200px',
                        click: () => {},
                    }} />
                </div>
                <div className="buttons__block">
                    <Button button_data={{
                        title: 'Статистика по менторам',
                        background: '#FFA500',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: true,
                        path: 'best',
                        minWidth: '200px',
                        click: () => {},
                    }} />
                </div>
                <div className="buttons__block">
                    <Button button_data={{
                        title: 'Ученики на ментора',
                        background: 'rgb(96 193 122)',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: true,
                        path: 'count_mentors_to_students',
                        minWidth: '200px',
                        click: () => {},
                    }} />
                </div>
                <div className="buttons__block">
                    <Button button_data={{
                        title: 'Статистика по заявкам',
                        background: '#c41e3a',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: true,
                        path: 'status_requests',
                        minWidth: '200px',
                        click: () => {},
                    }} />
                </div>
            </section>
            <Tags/>
        </div>
    );

}

export default Home;