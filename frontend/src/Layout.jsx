import React from 'react';
import './index.css';
import './reset.css';
import {Outlet} from "react-router-dom";
import { useNavigate, useLocation } from 'react-router-dom';
import Theme from './components/ui/Theme/Theme.jsx';


function Layout(props) {

  const navigate = useNavigate();
  const loc = useLocation();
  

  return (
    <div className='wrapper dark-theme'>
        <header className='header'>
          {loc.pathname !== '/login/' ? (
            <button type='button' className='prev' onClick={() => navigate(-1)}>Назад</button>
          ): (
            <button type='button' className='prev'></button>
          )}
          
          <Theme/>
        </header>
        <main className='main'>
            <Outlet />
        </main>
    </div>
  );
}

export default Layout;