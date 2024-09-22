// import { Link } from "react-router-dom";
import {
  MusicNoteBeamed,
  House,
  PatchQuestion,
  Search,
  Binoculars,
  PersonArmsUp,
  PersonCircle,
} from "react-bootstrap-icons";
import "./Sidebar.css";
import SidebarItem from "./SidebarItem";

const items = [
  { icon: <House size={35} className="mr-4 mb-2" />, title: "Home" },
  { icon: <PatchQuestion size={35} className="mr-4 mb-2" />, title: "Ask" },
  { icon: <Search size={35} className="mr-4 mb-2" />, title: "Search prompts" },
  {
    icon: <Binoculars size={35} className="mr-4 mb-2" />,
    title: "Find friends",
  },
  { icon: <PersonArmsUp size={35} className="mr-4 mb-2" />, title: "Friends" },
  { icon: <PersonCircle size={35} className="mr-4 mb-2" />, title: "Profile" },
];

function Sidebar(): JSX.Element {
  return (
    <div className="container">
      <div className="row sidebar-title float-start">
        <div className="menu-option">
          <MusicNoteBeamed size={40} className="mr-4" />
          <h1>PromptTunes</h1>
        </div>
      </div>
      <div className="mt-5 pt-3">
        {items.map((item) => (
          <SidebarItem key={item.title} icon={item.icon} title={item.title} />
        ))}
      </div>
    </div>
  );
}

export default Sidebar;
