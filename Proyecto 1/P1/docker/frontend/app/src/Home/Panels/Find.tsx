import { Button } from "react-bootstrap";
import Friend from "./Common/Friend";
import { useState } from "react";

function Find(): JSX.Element {
  const [searchTerm, setSearchTerm] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const friends = [
    {
      name: "Alice Smith",
      username: "aliceswiftie",
      bio: "✨ Taylor's version lover ✨ 🎤 Jamming to *Midnights* on repeat. 💖 Folklore and Evermore hit different. 🎶 Favorite lyrics: 'We could leave the Christmas lights up 'til January.' 🎤 Can't wait for the next tour! 📸 Sharing concert photos and my favorite merch. 💬 Let’s talk about Taylor's genius!",
      friends: 15,
      isFriend: true,
    },
    {
      name: "Bob Johnson",
      username: "swiftiebob",
      bio: "🎸 Rocking out to *Red* (Taylor’s Version) since day one! 🎤 Passionate about uncovering hidden Easter eggs in her music. 🎶 Favorite song: 'All Too Well (10 Minute Version).' 💖 Proud to be a part of #SwiftieNation.",
      friends: 20,
      isFriend: false,
    },
    {
      name: "Charlie Lee",
      username: "charlielee_13",
      bio: "🌟 #13Forever | Obsessed with *1989* vibes. 🎤 Favorite track: 'Style.' 💬 DM me for all things Taylor trivia! 🎶 Dreaming of a Taylor collab with Ed Sheeran. 🕰 Waiting for the next re-recorded album!",
      friends: 12,
      isFriend: true,
    },
    {
      name: "Dana White",
      username: "danataylorfan",
      bio: "🎶 *Speak Now* on repeat since it dropped. 💖 Big fan of Taylor’s songwriting evolution. 🎤 Favorite lyrics: 'I go back to December all the time.' 🕰 Counting down to the next Taylor surprise drop! 📸 Always ready for a new Taylor Swift meme!",
      friends: 8,
      isFriend: false,
    },
  ];

  // Group friends in pairs (two per row)
  const friendPairs = [];
  for (let i = 0; i < friends.length; i += 2) {
    friendPairs.push(friends.slice(i, i + 2));
  }

  const handleSearch = () => {
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
                      <Friend {...friend} />
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
