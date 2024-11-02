import { useState } from "react";
import { Button, Card } from "react-bootstrap";
import {
  PersonCircle,
  PersonAdd,
  PersonDash,
  PersonFillAdd,
  Pencil,
} from "react-bootstrap-icons";
import { followUser, updateProfile } from "../../../APICalls";
import EditProfileModal from "./EditProfileModal";

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
  const [showEditProfileModal, setShowEditProfileModal] = useState(false);

  const handleFollow = async () => {
    const response = await followUser(FriendProp.id);
    if (response.result === "error") {
      return;
    } else {
      setFollow(response.doesFollow);
      setFriends(response.friends);
    }
  };

  const handleSignOut = () => {
    localStorage.clear();
    window.location.assign("/");
  };

  const handleEdit = () => {
    setShowEditProfileModal(true);
  };

  const handleCloseEditProfileModal = () => {
    setShowEditProfileModal(false);
  };

  const handleSaveEditProfileModal = async (
    name: string,
    username: string,
    bio: string
  ) => {
    const response = await updateProfile(name, username, bio);

    if (response.result !== "error") {
      window.location.reload();
    }
  };

  return (
    <Card className="post-card friend">
      <Card.Body>
        <Card.Title className="d-flex align-items-center justify-content-between width-full post-user">
          <div d-flex align-items-center>
            <PersonCircle size={56} className="mr-4 user" />
            {FriendProp.name}
            {"  "}·{"  "}
            <span className="text-muted">{FriendProp.username}</span>
          </div>
          {FriendProp.isSelf && (
            <div className="ml-auto">
              <Button variant="link" onClick={handleEdit}>
                <Pencil color="#FFFFFF" size={28} />
              </Button>
              <Button variant="link" onClick={handleSignOut}>
                <PersonDash color="#FFFFFF" size={28} />
              </Button>
              <EditProfileModal
                curr_name={FriendProp.name}
                curr_username={FriendProp.username}
                curr_bio={FriendProp.bio}
                show={showEditProfileModal}
                handleClose={handleCloseEditProfileModal}
                handleSave={handleSaveEditProfileModal}
              />
            </div>
          )}
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
