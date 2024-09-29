import { Card } from "react-bootstrap";
import {
  PersonCircle,
  HandThumbsUp,
  HandThumbsUpFill,
} from "react-bootstrap-icons";
import "../Panels.css";
import { useState } from "react";

interface PostProps {
  PostUser: string;
  PostTime: string;
  PostPrompt: string;
  PostAnswer: string;
  PostLikes: number;
  hasBeenPosted?: boolean;
}

function Post({
  PostUser,
  PostTime,
  PostPrompt,
  PostAnswer,
  PostLikes,
  hasBeenPosted,
}: PostProps): JSX.Element {
  const [hasLiked, setHasLiked] = useState(false);
  const [likes, setLikes] = useState(PostLikes);
  const handleLike = () => {
    setHasLiked(!hasLiked);
    setLikes(likes + (hasLiked ? -1 : 1));
  };
  return (
    <Card className="post-card">
      <Card.Body>
        <Card.Title className="width-full post-user">
          <PersonCircle size={56} className="mr-4 user" />
          {PostUser}
          {"  "}·{"  "}
          <span className="text-muted">{PostTime}</span>
        </Card.Title>
        <Card.Text>
          <p>
            <span className="bold">Prompt:</span> {PostPrompt}
          </p>
        </Card.Text>
        <Card.Text className="post-content">
          <p>
            <span className="bold">Song:</span>{" "}
            <h3>{PostAnswer.split("\n")[0]}</h3>
            <p
              dangerouslySetInnerHTML={{
                __html: PostAnswer.split("\n").slice(1).join("<br>"),
              }}
            />
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
