import { useEffect } from 'react';
import { Routes, Route, useNavigate } from "react-router-dom";
import Layout from "./Layout.jsx";
import Login from "./components/pages/Login/Login.jsx";
import Home from "./components/pages/Home/Home.jsx";
// import Register from './components/pages/Register/Register.jsx';
import ChartPie from './components/ui/Chart/ChartPie.jsx';
import ChartBar from './components/ui/Chart/ChartBar.jsx';
import ChartMentors from './components/ui/Chart/ChartMentors.jsx';
import NotFound from './components/pages/NotFound/NotFound.jsx';
import ChartRequest from './components/ui/Chart/ChartRequest.jsx';


function App() {

    const Navigate = useNavigate();

    useEffect(() => {
        if(!localStorage.getItem('token')){
            Navigate('login/');
        }
    }, [])

    return (
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route index element={<Home />}/>
                <Route path="login/" element={<Login />}/>
                <Route path="count_mentors/" element={<ChartBar />}/>
                <Route path="best/" element={<ChartMentors />}/>
                <Route path="count_mentors_to_students/" element={<ChartPie />}/>
                <Route path="status_requests/" element={<ChartRequest />}/>
                <Route path='*' element={<NotFound/>}/>
                {/* <Route path="register/" element={<Register />}/> */}
            </Route>
        </Routes>
    )

}

export default App;
