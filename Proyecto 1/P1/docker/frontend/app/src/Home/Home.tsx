import { Route, Routes } from "react-router-dom";
import Sidebar from "./Sidebar/Sidebar";
import Ask from "./Panels/Ask";
import "./Home.css";

function Home() {
  return (
    <div className="main-container">
      <div className="main-div">
        <div className="sidebar-div">
          <Sidebar />
        </div>
        <div className="div-padding" />
        <div className="panels-div">
          <Routes>
            <Route path="/" element={<h1>Home</h1>} />
            <Route path="ask" element={<Ask />} />
            <Route path="search" element={<h1>Search prompts</h1>} />
            <Route path="find" element={<h1>Find friends</h1>} />
            <Route path="friends" element={<h1>Friends</h1>} />
            <Route path="profile" element={<h1>Profile</h1>} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default Home;
