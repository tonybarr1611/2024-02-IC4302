import { Button, Card, Modal } from "react-bootstrap";
import {
  PersonCircle,
  HandThumbsUp,
  HandThumbsUpFill,
  Pencil,
  Trash,
} from "react-bootstrap-icons";
import "../Panels.css";
import { useState } from "react";
import { deletePost, PromptResponse, sendLike } from "../../../APICalls";

interface PostProps {
  PostID?: string;
  PostUser: string;
  PostTime: string;
  PostPrompt: string;
  PostAnswer?: PromptResponse[];
  PostLikes: number;
  hasBeenPosted?: boolean;
  hasUserLiked?: boolean;
  isOwnPost?: boolean;
}

interface DeleteModalProps {
  show: boolean;
  handleClose: () => void;
  handleDelete: () => void;
}

function DeleteModal({
  show,
  handleClose,
  handleDelete,
}: DeleteModalProps): JSX.Element {
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

function Post({
  PostID,
  PostUser,
  PostTime,
  PostPrompt,
  PostAnswer,
  PostLikes,
  hasBeenPosted,
  hasUserLiked,
  isOwnPost,
}: PostProps): JSX.Element {
  const [hasLiked, setHasLiked] = useState(hasUserLiked || false);
  const [likes, setLikes] = useState(PostLikes);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  console.log(PostID);

  const handleLike = async () => {
    console.log(PostID);
    const response = await sendLike(PostID || "");

    if (response.result !== "error") {
      setHasLiked(!hasLiked);
      setLikes(likes + (hasLiked ? -1 : 1));
    }
  };

  const handleEdit = () => {
    console.log("edit");
  };

  const handleDelete = () => {
    setShowDeleteModal(true);
  };

  const handleCloseDelete = () => {
    setShowDeleteModal(false);
  };

  const handleDeleteConfirmed = async () => {
    const response = await deletePost(PostID || "");

    if (response.result !== "error") {
      window.location.reload();
    }
  };

  return (
    <Card className="post-card">
      <Card.Body>
        <Card.Title className="d-flex align-items-center justify-content-between width-full post-user">
          <div className="d-flex align-items-center">
            <PersonCircle size={56} className="mr-4 user" />
            {PostUser}
            {"  "}·{"  "}
            <span className="text-muted">{PostTime}</span>
          </div>
          {isOwnPost && (
            <div className="ml-auto">
              <Button variant="link" onClick={handleEdit}>
                <Pencil color="#FFFFFF" size={28} />
              </Button>
              <Button variant="link" onClick={handleDelete}>
                <Trash color="#FFFFFF" size={28} />
              </Button>
              <DeleteModal
                show={showDeleteModal}
                handleClose={handleCloseDelete}
                handleDelete={handleDeleteConfirmed}
              />
            </div>
          )}
        </Card.Title>
        <Card.Text>
          <p>
            <span className="bold">Prompt:</span> {PostPrompt}
          </p>
        </Card.Text>
        <Card.Text className="post-content">
          <p>
            <span className="bold">Answer:</span>{" "}
            {PostAnswer &&
              PostAnswer.map((answer, index) => (
                <div key={index}>
                  <h3>{answer.artist}</h3>
                  <h4>{answer.title}</h4>
                  <p
                    dangerouslySetInnerHTML={{
                      __html: answer.lyrics.split("\n").slice(1).join("<br>"),
                    }}
                  />
                </div>
              ))}
          </p>
        </Card.Text>
        <Card.Footer>
          {hasBeenPosted && (
            <p className="text-muted">
              <button className="like-btn" type="button" onClick={handleLike}>
                {hasLiked ? (
                  <HandThumbsUpFill
                    size={34}
                    className="mr-3"
                    color="#FFFFFF"
                  />
                ) : (
                  <HandThumbsUp size={34} className="mr-3" color="#FFFFFF" />
                )}
              </button>
              Likes: {likes}
            </p>
          )}
        </Card.Footer>
      </Card.Body>
    </Card>
  );
}

export type { PostProps };
export default Post;
