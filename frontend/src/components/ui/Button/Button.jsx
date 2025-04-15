import React, { useState } from 'react';
import { Link } from "react-router-dom";
import './Button.css';


function Button({
        button_data = {
            title: 'Button',
            background: '#000',
            color: '#fff',
            padding: '10px',
            borderRadius: '5px',
            maxWidth: '200px',
            click: () => {},
            is_link: false,
            path: '/',
        }
    }) {
    const [hover, setHover] = useState(false);

    // Динамические стили в зависимости от состояния hover
    const button_styles = {
        background: hover ? button_data.color : button_data.background,
        color: hover ? button_data.background : button_data.color,
        padding: button_data.padding,
        borderRadius: button_data.padding,
        maxWidth: button_data.maxWidth,
        minWidth: button_data.minWidth,
        border: `1px solid ${hover ? button_data.background : 'transparent'}`,
    };

    return (
        <>
            {button_data.is_link ? (
                <div className='wrap__button'>
                    <Link
                        to={button_data.path}
                        className="button"
                        style={button_styles}
                        onMouseEnter={() => setHover(true)}
                        onMouseLeave={() => setHover(false)}
                    >
                        {button_data.title}
                    </Link>
                </div>
            ) : (
                <div className='wrap__button'>
                    <button
                        className="button"
                        style={button_styles}
                        onMouseEnter={() => setHover(true)}
                        onMouseLeave={() => setHover(false)}
                        onClick={button_data.click}
                    >
                        {button_data.title}
                    </button>
                </div>
            )}
        </>
    );
}

export default Button;
