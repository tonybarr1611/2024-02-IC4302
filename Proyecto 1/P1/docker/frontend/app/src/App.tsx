import "./bootstrap/bootstrap.min.css";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";
import Login from "./Login/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home/Home";

function App() {
  return (
    <div className="background">
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home/*" element={<Home />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
