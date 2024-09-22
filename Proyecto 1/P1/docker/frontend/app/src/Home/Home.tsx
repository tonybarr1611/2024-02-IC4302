import { Route, Routes } from "react-router-dom";
import Sidebar from "./Sidebar/Sidebar";
import Ask from "./Panels/Ask";
import Search from "./Panels/Search";
import "./Home.css";
import Feed from "./Panels/Common/Feed";
import Find from "./Panels/Find";

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
            <Route path="/" element={<Feed />} />
            <Route path="ask" element={<Ask />} />
            <Route path="search" element={<Search />} />
            <Route path="find" element={<Find />} />
            <Route path="friends" element={<h1>Friends</h1>} />
            <Route path="profile" element={<h1>Profile</h1>} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default Home;
