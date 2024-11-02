import { Button } from "react-bootstrap";
import Friend, { FriendProps } from "./Common/Friend";
import { useState } from "react";
import { findFriends } from "../../APICalls";

function Find(): JSX.Element {
  const [searchTerm, setSearchTerm] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  // Stored as pairs of friends to display two per row
  const [friendPairs, setFriendPairs] = useState<FriendProps[][]>([]);

  // Group friends in pairs (two per row)

  const handleSearch = async () => {
    const response = await findFriends(searchTerm);
    const tempPairs: FriendProps[][] = [];
    for (let i = 0; i < response.length; i += 2) {
      tempPairs.push(response.slice(i, i + 2));
    }
    setFriendPairs(tempPairs);
    setHasSearched(true);
  };

  return (
    <div className="panel">
      <h1>Find</h1>
      <p className="subtitles">Find new friends</p>
      <div className="">
        <form className="width-full">
          <label className="mt-4">
            <p>Type your search here!</p>
          </label>
          <textarea
            placeholder="Type your search here"
            className="ask-input"
            cols={30}
            rows={3}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <Button
            variant="primary"
            className="w-100 mb-3"
            onClick={handleSearch}
          >
            Search!
          </Button>
          {hasSearched && (
            <div className="container">
              {friendPairs.map((pair, index) => (
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
                        isSelf={false}
                      />
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default Find;
