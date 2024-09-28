import { Card } from "react-bootstrap";
import {
  PersonCircle,
  HandThumbsUp,
  HandThumbsUpFill,
} from "react-bootstrap-icons";
import "../Panels.css";
import { useState } from "react";
import { PromptResponse, sendLike } from "../../../APICalls";

interface PostProps {
  PostID?: string;
  PostUser: string;
  PostTime: string;
  PostPrompt: string;
  PostAnswer?: PromptResponse[];
  PostLikes: number;
  hasBeenPosted?: boolean;
  hasUserLiked?: boolean;
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
}: PostProps): JSX.Element {
  const [hasLiked, setHasLiked] = useState(hasUserLiked || false);
  const [likes, setLikes] = useState(PostLikes);
  console.log(PostID);

  const handleLike = async () => {
    console.log(PostID);
    const response = await sendLike(PostID || "");

    if (response.result !== "error") {
      setHasLiked(!hasLiked);
      setLikes(likes + (hasLiked ? -1 : 1));
    }
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
