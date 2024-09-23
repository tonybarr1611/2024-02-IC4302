import { useState } from "react";
import { Card } from "react-bootstrap";
import { PersonCircle, PersonAdd, PersonFillAdd } from "react-bootstrap-icons";

type FriendProps = {
  name: string;
  username: string;
  bio: string;
  friends: number;
  isFriend: boolean;
  isSelf?: boolean;
};

function Friend(props: FriendProps): JSX.Element {
  const [follow, setFollow] = useState(props.isFriend);
  const [friends, setFriends] = useState(props.friends);

  const handleFollow = () => {
    setFollow(!follow);
    setFriends(follow ? friends - 1 : friends + 1);
  };

  return (
    <Card className="post-card friend">
      <Card.Body>
        <Card.Title className="width-full post-user">
          <PersonCircle size={56} className="mr-4 user" />
          {props.name}
          {"  "}·{"  "}
          <span className="text-muted">{props.username}</span>
        </Card.Title>
        <Card.Text>
          <p>
            <span className="bold">Biography:</span> {props.bio}
          </p>
        </Card.Text>
        <Card.Text>
          <p>
            <span className="bold">Friends:</span> {friends}
          </p>
        </Card.Text>
        <Card.Footer>
          {!props.isSelf && (
            <p className="text-muted">
              <button className="like-btn" type="button" onClick={handleFollow}>
                {follow ? (
                  <PersonFillAdd size={34} className="mr-3" color="#FFFFFF" />
                ) : (
                  <PersonAdd size={34} className="mr-3" color="#FFFFFF" />
                )}
              </button>
            </p>
          )}
        </Card.Footer>
      </Card.Body>
    </Card>
  );
}

export default Friend;
