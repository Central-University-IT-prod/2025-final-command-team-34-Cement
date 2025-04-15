import { createRoot } from 'react-dom/client';
import App from "./App.jsx";
import {BrowserRouter} from "react-router-dom";

const HostBackend = 'http://prod-team-34-rqpd9aim.REDACTED/api/';


export function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim(); // Удаляет пробелы в начале и конце строки
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


createRoot(document.getElementById('root')).render(
    <BrowserRouter>
        <App />
    </BrowserRouter>
)

export default HostBackend;