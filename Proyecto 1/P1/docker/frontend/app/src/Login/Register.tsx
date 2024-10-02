import React, { useState } from "react";
import { Button, Card, Col, Container, Form, Row } from "react-bootstrap";
import { toast, ToastContainer } from "react-toastify";
import { EyeFill, EyeSlashFill, PersonPlus } from "react-bootstrap-icons";
import "./Register.css";
import { Link } from "react-router-dom";
import { sendRegister } from "../APICalls";

// Define the shape of the registration details object
interface RegistrationDetails {
  name: string;
  username: string;
  email: string;
  password: string;
}

function Register(): React.JSX.Element {
  // State to hold the registration details
  const [details, setDetails] = useState<RegistrationDetails>({
    name: "",
    username: "",
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
    const response = await sendRegister(
      details.name,
      details.username,
      details.email,
      details.password
    );

    if (response.result === "error") {
      toast.error("Registration failed", {
        autoClose: 1500,
        theme: "colored",
      });
      setDetails({ name: "", username: "", email: "", password: "" });
    } else {
      toast.success("Registered successfully", {
        autoClose: 1500,
        theme: "colored",
      });
      window.location.href = "/home";
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center container-register">
      {/* Toast container for notifications */}
      <ToastContainer position="top-center" />
      <Card className="card-register">
        <Card.Body>
          <div className="text-center mb-4">
            {/* Icon and title for the register card */}
            <PersonPlus size={40} className="mb-3 icon-register" />
            <h1 className="h4">Register</h1>
          </div>
          {/* Form for user registration */}
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3 leftText" controlId="formBasicName">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter name"
                name="name"
                value={details.name}
                onChange={(e) =>
                  setDetails({ ...details, name: e.target.value })
                }
              />
            </Form.Group>
            <Form.Group className="mb-3 leftText" controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                name="username"
                value={details.username}
                onChange={(e) =>
                  setDetails({ ...details, username: e.target.value })
                }
              />
            </Form.Group>
            <Form.Group className="mb-3 leftText" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                name="email"
                value={details.email}
                onChange={(e) =>
                  setDetails({ ...details, email: e.target.value })
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
                  value={details.password}
                  onChange={(e) =>
                    setDetails({
                      ...details,
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
              Register
            </Button>
            <Link to={"/"}>
              <Row>
                <Col className="text-end">
                  <span className="guest-login">
                    Already have an account? Sign In
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

export default Register;
