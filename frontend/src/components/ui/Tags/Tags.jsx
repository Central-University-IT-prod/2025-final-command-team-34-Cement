import React, {useState, useEffect, useRef} from 'react';
import Title from '../../ui/Title/Title.jsx';
import './Tags.css';
import Button from '../Button/Button.jsx';
import Input from '../Input/Input.jsx';
import Message from '../Message/Message.jsx';
import axios from 'axios';
import HostBackend from '../../../main.jsx';
import { getCookie } from '../../../main.jsx';


function Tags(props) {

    const [messageOpen, setMessageOpen] = useState(false);
    const timerId = useRef(null); // Храним идентификатор таймера
    const [tags, setTags] = useState([]);
    const [modal, setModal] = useState(false);
    const [tagName, setTagName] = useState('');
    const [tagNameError, setTagNameError] = useState(false);

    useEffect(()=>{
        axios.get(`${HostBackend}analytics/mentors/tags/`)
        .then(response => {
            setTags(response.data);
        })
    }, []);

    const handleAddTag = () => {

        if(tagName.length === 0){
            setTagNameError('Введите название тега');
            return;
        }

        if(tags.some(tag => tag.name.toLowerCase() === tagName.toLowerCase())){
            setTagNameError('Тег с таким названием уже существует');
            return;
        }

        setTagNameError('');

        axios.post(`${HostBackend}tags/`, {
            name: tagName,
        },{
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            // withCredentials: true
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });

        setModal(false);
        setTags([...tags, {id: tags[tags.length-1].id + 1, name: tagName, mentors: 0}]);
        setTagName('');
        
        setMessageOpen(true);
        // Если таймер уже запущен, сбрасываем его
        if (timerId.current) {
            clearTimeout(timerId.current);
        }

        // Запускаем новый таймер
        timerId.current = setTimeout(() => {
            setMessageOpen(false);
        }, 4000);

    };

    return (
        <div className='tags__container'>
            <Title name='Список тегов' />   
            <ul className='tags'>
                {tags.map((item)=>(
                    <li key={item.id} className='tags__item'>{item.name} {item.mentors !== 0 && `- ${item.mentors} Мен.`}</li>
                ))}
            </ul>
            <div className="add_tag">
                <Button button_data={{
                    title: 'Добавить тег',
                    background: 'var(--color-blue)',
                    color: 'var(--color-white)',
                    padding: '12px',
                    maxWidth: '250px',
                    is_link: false,
                    click: ()=>{setModal(true); window.scroll({top: 0});},
                }} />
            </div>
            <div className="overlay" onClick={()=>{setModal(false);setTagNameError('');}}></div>
            {modal && (
                <div className="modal">
                    <Input input_data={{
                        type: 'text',
                        placeholder: 'Введите название тега',
                        value: tagName,
                        onChange: (e) => setTagName(e.target.value),
                        error: tagNameError,
                    }} />

                    <Button button_data={{
                        title: 'Добавить',
                        background: '#00BC00',
                        color: 'var(--color-white)',
                        padding: '12px',
                        is_link: false,
                        click: handleAddTag
                    }} />
                </div>
            )}
            <Message message_open={messageOpen} name='Успешно добавлено'/>
        </div>
    );

}

export default Tags;