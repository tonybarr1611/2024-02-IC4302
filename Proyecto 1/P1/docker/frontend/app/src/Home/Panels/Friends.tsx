import { useEffect, useState } from "react";
import Friend, { FriendProps } from "./Common/Friend";
import { getFriends } from "../../APICalls";

function Friends(): JSX.Element {
  const [friendsPairs, setFriendsPairs] = useState<FriendProps[][]>([]);

  useEffect(() => {
    const fetchFriends = async () => {
      const response = await getFriends();
      const tempPairs: FriendProps[][] = [];
      for (let i = 0; i < response.length; i += 2) {
        tempPairs.push(response.slice(i, i + 2));
      }
      setFriendsPairs(tempPairs);
    };
    fetchFriends();
  }, []);

  return (
    <div className="panel">
      <h1>Friends</h1>
      <p className="subtitles">Look at your friends</p>
      <div className="container">
        {friendsPairs.map((pair, index) => (
          <div className="row" key={index}>
            {pair.map((friend, subIndex) => (
              <div className="col mr-4 mb-5" key={subIndex}>
                <Friend
                  id={friend.id}
                  name={friend.name}
                  username={friend.username}
                  bio={friend.bio}
                  friends={friend.friends}
                  isFriend={friend.isFriend}
                />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Friends;
