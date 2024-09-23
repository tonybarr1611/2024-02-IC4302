import { useState } from "react";
import { Button } from "react-bootstrap";
import Post, { PostProps } from "./Common/Post";

function Search(): JSX.Element {
  const [searchTerm, setSearchTerm] = useState("");
  const [results, setResults] = useState<PostProps[]>([]);

  const handleSearch = () => {
    const searchElement = document.getElementsByName(
      "search"
    )[0] as HTMLTextAreaElement;
    // Create a mock object using the search term and PostProps interface
    // interface PostProps {
    //   PostUser: string;
    //   PostTime: string;
    //   PostPrompt: string;
    //   PostAnswer: string;
    //   PostLikes: number;
    //   hasBeenPosted?: boolean;
    // }
    const mockResults: PostProps[] = Array.from({ length: 20 }, () => ({
      PostUser: "MockUser",
      PostTime: new Date().toISOString(),
      PostPrompt: searchTerm,
      PostAnswer: "This is a mock result",
      PostLikes: 0,
      hasBeenPosted: true,
    }));
    setResults(mockResults);
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
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button variant="primary" className="w-100 mb-3" onClick={handleSearch}>
          Search!
        </Button>
        {results.map((result, index) => (
          <div className="mt-1">
            <Post
              key={index}
              PostUser={result.PostUser}
              PostTime={result.PostTime}
              PostPrompt={result.PostPrompt}
              PostAnswer={result.PostAnswer}
              PostLikes={result.PostLikes}
              hasBeenPosted={result.hasBeenPosted}
            />
          </div>
        ))}
      </form>
    </div>
  );
}

export default Search;
