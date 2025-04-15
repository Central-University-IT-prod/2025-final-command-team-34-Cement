import React, { useEffect, useState } from 'react';
import './Theme.css';


function Theme(props) {
    
    const [theme, setTheme] = useState(
        localStorage.getItem('theme') || 'white'
    );

    useEffect(() => {
        // Применяем тему при загрузке компонента
        applyTheme(theme);
    }, []); // Пустой массив зависимостей, чтобы эффект выполнился только при монтировании

    useEffect(() => {
        // Сохраняем тему в localStorage и применяем её при изменении
        localStorage.setItem('theme', theme);
        applyTheme(theme);
    }, [theme]);

    const applyTheme = (theme) => {
        const wrapper = document.querySelector('.wrapper');
        if (wrapper) {
            wrapper.classList.remove('light-theme', 'dark-theme');
            if (theme === 'white') {
                wrapper.classList.add('light-theme');
            } else {
                wrapper.classList.add('dark-theme');
            }
        }
    };

    return (
        <button
            type='button'
            className='theme'
            onClick={() => {
                setTheme(theme === 'white' ? 'black' : 'white');
            }}
        >
            {theme === 'white' ? '☀️' : '🌙'} {/* Солнце для светлой темы, луна для темной */}
        </button>
    );
}

export default Theme;