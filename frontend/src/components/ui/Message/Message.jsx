import React, {useRef} from 'react';
import './Message.css';


function Message(props) {

    return (
        <span className={props.message_open ? 'message message--active' : 'message'}>
            {props.name}
        </span>
    );
}

export default Message;