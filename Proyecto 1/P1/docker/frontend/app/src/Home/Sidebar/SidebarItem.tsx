import { Link } from "react-router-dom";
import "./Sidebar.css";
type Props = { icon: React.ReactElement; title: string };

function SidebarItem({ icon: Icon, title }: Props): JSX.Element {
  var path = title.split(" ")[0].toLowerCase();
  if (path === "home") {
    path = "";
  }
  return (
    <Link to={path} style={{ all: "unset" }}>
      <div className="row sidebar-title float-start mt-3">
        <div className="menu-option hover-option">
          {Icon}
          <h2>{title}</h2>
        </div>
      </div>
    </Link>
  );
}

export default SidebarItem;
