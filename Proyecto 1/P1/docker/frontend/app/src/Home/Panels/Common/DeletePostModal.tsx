import { Modal, Button } from "react-bootstrap";
import "../Panels.css";

interface DeletePostModalProps {
  show: boolean;
  handleClose: () => void;
  handleDelete: () => void;
}

function DeletePostModal({
  show,
  handleClose,
  handleDelete,
}: DeletePostModalProps): JSX.Element {
  return (
    <Modal
      show={show}
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
      className="dark-modal"
    >
      <Modal.Header closeButton>
        <Modal.Title>Confirm Deletion</Modal.Title>
      </Modal.Header>
      <Modal.Body>Are you sure you want to delete this post?</Modal.Body>
      <Modal.Footer>
        <Button className="btn-cancel" variant="link" onClick={handleClose}>
          Cancel
        </Button>
        <Button className="btn-delete" variant="link" onClick={handleDelete}>
          Confirm Delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default DeletePostModal;
