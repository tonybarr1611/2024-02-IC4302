import "./bootstrap/bootstrap.min.css";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";
import Login from "./Login/Login";

function App() {
  return (
    <div style={{ backgroundColor: "#363A3F", width: "100%", height: "100%" }}>
      <Login></Login>
    </div>
  );
}

export default App;
