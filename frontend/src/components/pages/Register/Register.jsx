import React, {useState} from 'react';
import Title from "../../ui/Title/Title.jsx";
import Input from "../../ui/Input/Input.jsx";
import Button from "../../ui/Button/Button.jsx";
import {getCookie} from "../../../main.jsx";
import {useNavigate } from "react-router-dom";
import HostBackend from "../../../main.jsx";
import axios from 'axios';


function Register(props) {

    const Navigate = useNavigate();
    const [userName, setUserName] = useState('');
    const [userNameError, setUserNameError] = useState('');
    const [userPassword, setUserPassword] = useState('');
    const [userPasswordError, setUserPasswordError] = useState('');
    // const [userPassword2, setUserPassword2] = useState('');
    // const [userEmail, setUserEmail] = useState('');
    // const [userEmailError, setUserEmailError] = useState('');

    const handleSubmit = () => {

        if(userName === ''){
            setUserNameError('Это обязательное поле');
            return;
        }

        setUserNameError('');

        if(userPassword === ''){
            setUserPasswordError('Это обязательное поле');
            return;
        }

        if(userPassword.length < 8){
            setUserPasswordError('Слишком короткий пароль, минимум 8 символов');
            return;
        }

        // if(userPassword2 !== userPassword){
        //     setUserPasswordError('Пароли не совпадают')
        //     return;
        // }

        setUserPasswordError('');

        // if(userEmail === ''){
        //     setUserEmailError('Это обязательное поле');
        //     return;
        // }

        // if(!userEmail.includes('@') && !userEmail.includes('.')){
        //     setUserEmailError('Неправильный формат');
        //     return;
        // }

        // setUserEmailError('');

        axios.post(`${HostBackend}auth/`, {
            login: userName,
            // email: userEmail,
            password: userPassword,
        }, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            withCredentials: true,
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
            console.error("Error fetching services:", error);
        });
    }

    return (
        <div className='login'>
            <Title name='Регистрация'/>
            <p className='login__description'>Введите свои данные для регистрации</p>
            <section className="login__inputs">
                <Input input_data={{
                    title: 'Ваш логин',
                    type: 'text',
                    placeholder: 'Sigmaboy228',
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
                {/* <Input input_data={{
                    title: 'Ваш пароль еще раз',
                    type: 'password',
                    placeholder: '* * * * * * * *',
                    value: userPassword2,
                    onChange: (e) => setUserPassword2(e.target.value),
                    error: userPasswordError,
                }} /> */}
                {/* <Input input_data={{
                    title: 'Ваш e-mail',
                    type: 'email',
                    placeholder: 'example@gmail.com',
                    value: userEmail,
                    onChange: (e) => setUserEmail(e.target.value),
                    error: userEmailError,
                }} /> */}
                <div className="login__buttons">
                    <Button button_data={{
                        title: 'Создать аккаунт',
                        background: 'var(--color-blue)',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: false,
                        click: handleSubmit
                    }} />
                    <Button button_data={{
                        title: 'У меня есть аккаунт',
                        background: 'var(--color-white)',
                        color: 'var(--color-blue)',
                        padding: '12px',
                        is_link: true,
                        path: '/login/',
                        click: handleSubmit
                    }} />
                </div>
            </section>
        </div>
    );

}

export default Register;