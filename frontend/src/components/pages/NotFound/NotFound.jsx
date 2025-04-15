import React from 'react';
import Title from '../../ui/Title/Title';
import { Link } from 'react-router-dom';
import Button from '../../ui/Button/Button';
import './NotFound.css';


function NotFound() {

    return (
        <div className='not_found'>
            <Title name='Такой страницы не найдено' />
            <Button button_data={{
                title: 'На главную',
                background: 'var(--color-blue)',
                color: 'var(--color-white)',
                padding: '12px',
                is_link: true,
                path: '/',
                click: ()=>{},
            }} />
        </div>
    );
    
}

export default NotFound;
