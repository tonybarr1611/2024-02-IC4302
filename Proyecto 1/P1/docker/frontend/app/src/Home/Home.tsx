import { Route, Routes } from "react-router-dom";
import Sidebar from "./Sidebar/Sidebar";
import Ask from "./Panels/Ask";
import Search from "./Panels/Search";
import "./Home.css";
import Feed from "./Panels/Common/Feed";
import Find from "./Panels/Find";
import Profile from "./Panels/Profile";
import Friends from "./Panels/Friends";
import Edit from "./Panels/Edit";

function Home() {
  // Redirect to login if user_id is not set
  if (localStorage.getItem("user_id") === null) {
    window.location.href = "/";
  }
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
            <Route path="friends" element={<Friends />} />
            <Route path="profile" element={<Profile />} />
            <Route path="edit" element={<Edit />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default Home;
