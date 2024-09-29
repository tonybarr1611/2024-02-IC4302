import { Button, Card } from "react-bootstrap";
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
import DeletePostModal from "./DeletePostModal";
import { useNavigate } from "react-router-dom";

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
  const [showDeletePostModal, setShowDeletePostModal] = useState(false);

  const navigate = useNavigate();

  const handleLike = async () => {
    const response = await sendLike(PostID || "");

    if (response.result !== "error") {
      setHasLiked(!hasLiked);
      setLikes(likes + (hasLiked ? -1 : 1));
    }
  };

  const handleEdit = () => {
    navigate("/home/edit", { state: { id: PostID, curr_prompt: PostPrompt } });
  };

  const handleDelete = () => {
    setShowDeletePostModal(true);
  };

  const handleCloseDelete = () => {
    setShowDeletePostModal(false);
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
              <DeletePostModal
                show={showDeletePostModal}
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
