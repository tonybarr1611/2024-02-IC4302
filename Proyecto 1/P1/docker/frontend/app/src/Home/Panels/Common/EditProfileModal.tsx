import { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import "../Panels.css";

interface EditProfileModalProps {
  curr_name: string;
  curr_username: string;
  curr_bio: string;
  show: boolean;
  handleClose: () => void;
  handleSave: (name: string, username: string, bio: string) => void;
}

function EditProfileModal({
  curr_name,
  curr_username,
  curr_bio,
  show,
  handleClose,
  handleSave,
}: EditProfileModalProps): JSX.Element {
  // State to manage the form inputs
  const [name, setName] = useState<string>(curr_name);
  const [username, setUsername] = useState<string>(curr_username);
  const [bio, setBio] = useState<string>(curr_bio);

  const handleSaveClick = () => {
    handleSave(name, username, bio);
    handleClose();
  };

  return (
    <Modal
      show={show}
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
      className="dark-modal"
    >
      <Modal.Header closeButton>
        <Modal.Title>Edit Profile</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formName">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter your name"
              className="ask-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="formUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter your username"
              className="ask-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="formBio">
            <Form.Label>Biography</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder="Tell us about yourself"
              className="ask-input"
              value={bio}
              onChange={(e) => setBio(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button className="btn-cancel" variant="link" onClick={handleClose}>
          Cancel
        </Button>
        <Button className="btn-save" variant="link" onClick={handleSaveClick}>
          Save Changes
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default EditProfileModal;
