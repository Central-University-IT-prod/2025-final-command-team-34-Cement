import React, {useState} from 'react';
import axios from "axios";
import Title from "../../ui/Title/Title.jsx";
import Input from "../../ui/Input/Input.jsx";
import Button from "../../ui/Button/Button.jsx";
import {getCookie} from "../../../main.jsx";
import {useNavigate} from "react-router-dom";
import HostBackend from "../../../main.jsx";
import './Login.css';


function Login(props) {

    const Navigate = useNavigate(); 
    const [userPassword, setUserPassword] = useState('');
    const [userPasswordError, setUserPasswordError] = useState('');
    const [userName, setUserName] = useState('');
    const [userNameError, setUserNameError] = useState('');

    const handleSubmit = () => {

        if(userName === ''){
            setUserNameError('Это поле обязательно');
            return;
        }

        setUserNameError('');

        if(userPassword === ''){
            setUserPasswordError('Это поле обязательно');
            return;
        }

        setUserPasswordError('');

        axios.post(`${HostBackend}auth/login/`, {
            'login': userName,
            'password': userPassword,
        }, {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        // withCredentials: true,
        })
        .then(response => {
            if(response.detail){
                setUserNameError(response.data.detail);
                return;
            }
            
            Navigate('/');
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('role', response.data.role);
        })
        .catch(error => {
            setUserNameError('Неверный логин или пароль');
        });
    }

    return (
        <div className='login'>
            <Title name='Вход'/>
            <p className='login__description'>Введите свои данные для авторизации</p>
            <section className="login__inputs">
                <Input input_data={{
                    title: 'Ваш логин',
                    type: 'text',
                    placeholder: 'Login',
                    value: userName,
                    onChange: (e) => setUserName(e.target.value),
                    error: userNameError,
                }} />
                <Input input_data={{
                    title: 'Ваш пароль',
                    type: 'password',
                    placeholder: '* * * * * * * *',
                    value: userPassword,
                    onChange: (e) => setUserPassword(e.target.value),
                    error: userPasswordError,
                }} />
                <div className="login__buttons">
                    <Button button_data={{
                        title: 'Вход',
                        background: 'var(--color-blue)',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: false,
                        click: handleSubmit,
                    }} />
                    {/* <Button button_data={{
                        title: 'Создать аккаунт',
                        background: 'var(--color-white)',
                        color: 'var(--color-blue)',
                        padding: '12px',
                        is_link: true,
                        path: '/register/',
                        click: () => {},
                    }} /> */}
                </div>
            </section>
        </div>
    );
}

export default Login;