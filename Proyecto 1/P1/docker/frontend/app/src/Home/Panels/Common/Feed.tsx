import { useEffect, useState } from "react";
import Post, { PostProps } from "./Post";
import { getFeed } from "../../../APICalls";

function Feed(): JSX.Element {
  const [posts, setPosts] = useState<PostProps[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getFeed();
      setPosts(data);
    };
    fetchData();
  }, []);

  return (
    <div className="panel">
      <h1>Feed</h1>
      <p className="subtitles">Look at your friends' posts</p>
      {posts.map((post, index) => (
        <div className="mt-1">
          <Post
            key={index}
            PostID={post.PostID}
            PostUser={post.PostUser}
            PostTime={post.PostTime}
            PostPrompt={post.PostPrompt}
            PostAnswer={post.PostAnswer}
            PostLikes={post.PostLikes}
            hasBeenPosted={post.hasBeenPosted}
            hasUserLiked={post.hasUserLiked}
          />
        </div>
      ))}
    </div>
  );
}

export default Feed;
