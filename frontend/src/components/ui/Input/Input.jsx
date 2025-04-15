import React, {useState} from 'react';
import VisiblePasswordImage from '../../../assets/icons/visible_password.svg';
import HiddenPasswordImage from '../../../assets/icons/hidden_password.svg';
import './Input.css';


function Input(props) {

    const [passwordVisible, setPasswordVisible] = useState(false);

    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    return (
        <label className='label'>
            <span className="label__content">
                {props.input_data.title}
                <input
                    type={
                      props.input_data.type === 'password'
                        ? (passwordVisible ? "text" : "password")
                        : props.input_data.type
                    }
                    placeholder={props.input_data.placeholder}
                    value={props.input_data.value || ''}
                    onChange={props.input_data.onChange}
                    readOnly={props.input_data.readonly}
                    className='label__input' required
                />
                {props.input_data.type === 'password' && (
                    <button type='button' className='visible_password' onClick={togglePasswordVisibility}>
                      {passwordVisible ? (
                          <img
                              src={HiddenPasswordImage}
                              alt="Показать пароль"
                              width='20'
                              height='20'
                              className='visible_password__image'
                          />
                      ): (
                          <img
                              src={VisiblePasswordImage}
                              alt="Скрыть пароль"
                              width='20'
                              height='20'
                              className='visible_password__image'
                          />
                      )}
                    </button>
                )}
            </span>
            {props.input_data.error && (
                <span className="input_error">{props.input_data.error}</span>
            )}

        </label>
    );

}

export default Input;