import { useState } from "react";
import { Card } from "react-bootstrap";
import { PersonCircle, PersonAdd, PersonFillAdd } from "react-bootstrap-icons";
import { followUser } from "../../../APICalls";

type FriendProps = {
  id: string;
  name: string;
  username: string;
  bio: string;
  friends: number;
  isFriend: boolean;
  isSelf?: boolean;
};

function Friend(FriendProp: FriendProps): JSX.Element {
  const [follow, setFollow] = useState(FriendProp.isFriend);
  const [friends, setFriends] = useState(FriendProp.friends);

  const handleFollow = async () => {
    const response = await followUser(FriendProp.id);
    console.log(response);
    console.log(response.result);
    if (response.result === "error") {
      return;
    } else {
      setFollow(response.doesFollow);
      setFriends(response.friends);
    }
  };

  return (
    <Card className="post-card friend">
      <Card.Body>
        <Card.Title className="width-full post-user">
          <PersonCircle size={56} className="mr-4 user" />
          {FriendProp.name}
          {"  "}·{"  "}
          <span className="text-muted">{FriendProp.username}</span>
        </Card.Title>
        <Card.Text>
          <p className="mt-4">
            <span className="bold">Biography:</span> {FriendProp.bio}
          </p>
        </Card.Text>
        <Card.Text>
          <p>
            <span className="bold">Friends:</span> {friends}
          </p>
        </Card.Text>
        <Card.Footer>
          {!FriendProp.isSelf && (
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

export type { FriendProps };
export default Friend;
