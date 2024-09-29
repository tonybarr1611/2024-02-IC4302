import { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import Post, { PostProps } from "./Common/Post";
import { search } from "../../APICalls";

function Search(): JSX.Element {
  const [searchTerm, setSearchTerm] = useState("");
  const [results, setResults] = useState<PostProps[]>([]);

  useEffect(() => {
    async function fetchData() {
      const posts = await search(searchTerm);
      setResults(posts);
    }
    fetchData();
  }, [searchTerm]);

  const handleSearch = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    const search = document.querySelector(".ask-input") as HTMLInputElement;
    setSearchTerm(search.value);
  };

  return (
    <div className="panel">
      <h1>Search PrompTunes</h1>
      <p className="subtitles">Search for prompts and songs!</p>
      <form className="width-full">
        <label className="mt-4">
          <p>Type your search here!</p>
        </label>
        <textarea
          placeholder="Type your search here"
          className="ask-input"
          cols={30}
          rows={3}
        />
        <Button variant="primary" className="w-100 mb-3" onClick={handleSearch}>
          Search!
        </Button>
        {results.map((result, index) => (
          <div className="mt-1">
            <Post
              key={index}
              PostID={result.PostID}
              PostUser={result.PostUser}
              PostTime={result.PostTime}
              PostPrompt={result.PostPrompt}
              PostAnswer={result.PostAnswer}
              PostLikes={result.PostLikes}
              hasBeenPosted={result.hasBeenPosted}
              hasUserLiked={result.hasUserLiked}
            />
          </div>
        ))}
      </form>
    </div>
  );
}

export default Search;
