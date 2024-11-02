import React, { useState } from "react";
import { Button, Card, Col, Container, Form, Row } from "react-bootstrap";
import { ToastContainer, toast } from "react-toastify";
import { EyeFill, EyeSlashFill, PersonLock } from "react-bootstrap-icons";
import { Link } from "react-router-dom";
import { sendLogin } from "../APICalls";
import "./Login.css";

// Define the shape of the credentials object
interface Credentials {
  email: string;
  password: string;
}

function Login(): React.JSX.Element {
  // State to hold the email and password
  const [credentials, setCredentials] = useState<Credentials>({
    email: "",
    password: "",
  });

  // State to toggle password visibility
  const [showPassword, setShowPassword] = useState(false);

  // Function to handle the password visibility toggle
  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const response = await sendLogin(credentials.email, credentials.password);
    if (response.result === "error") {
      toast.error("Invalid email or password", {
        autoClose: 1500,
        theme: "colored",
      });
      setCredentials({ email: "", password: "" });
    } else {
      toast.success("Logged in successfully", {
        autoClose: 1500,
        theme: "colored",
      });
      window.location.href = "/home";
    }
  };

  localStorage.clear();

  return (
    <Container className="d-flex justify-content-center align-items-center container-login">
      {/* Toast container for notifications */}
      <ToastContainer position="top-center" />
      <Card className="card-login">
        <Card.Body>
          <div className="text-center mb-4">
            {/* Icon and title for the login card */}
            <PersonLock size={40} className="mb-3 icon-login" />
            <h1 className="h4">Sign In</h1>
          </div>
          {/* Form for user login */}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3 leftText" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                name="email"
                value={credentials.email}
                onChange={(e) =>
                  setCredentials({ ...credentials, email: e.target.value })
                }
              />
            </Form.Group>
            <Form.Group className="mb-3 leftText" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <div className="input-group">
                <Form.Control
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  name="password"
                  value={credentials.password}
                  onChange={(e) =>
                    setCredentials({
                      ...credentials,
                      password: e.target.value,
                    })
                  }
                />
                <Button
                  variant="primary"
                  onClick={handleClickShowPassword}
                  className="ml-1"
                >
                  {showPassword ? <EyeSlashFill /> : <EyeFill />}
                </Button>
              </div>
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100 mb-3">
              Sign In
            </Button>
            <Link to={"register"}>
              <Row>
                <Col className="text-end">
                  <span
                    className="guest-login"
                    onClick={() =>
                      toast.success("Logged in as guest", {
                        autoClose: 1500,
                        theme: "colored",
                      })
                    }
                  >
                    Register
                  </span>
                </Col>
              </Row>
            </Link>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
}

export default Login;
