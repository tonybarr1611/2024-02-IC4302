import { useEffect, useState } from "react";
import Post, { PostProps } from "./Post";

function Feed(): JSX.Element {
  const [posts, setPosts] = useState<PostProps[]>([]);

  const fillPostsWithMockData = () => {
    const mockResults: PostProps[] = Array.from({ length: 20 }, () => ({
      PostUser: "MockUser",
      PostTime: new Date().toISOString(),
      PostPrompt: "This is a mock prompt",
      PostAnswer: "This is a mock result",
      PostLikes: 1,
      hasBeenPosted: true,
    }));
    setPosts(mockResults);
  };
  useEffect(() => {
    fillPostsWithMockData();
  }, []);
  return (
    <div className="panel">
      <h1>Feed</h1>
      <p className="subtitles">Look at your friends' posts</p>
      {posts.map((post, index) => (
        <div className="mt-1">
          <Post
            key={index}
            PostUser={post.PostUser}
            PostTime={post.PostTime}
            PostPrompt={post.PostPrompt}
            PostAnswer={post.PostAnswer}
            PostLikes={post.PostLikes}
            hasBeenPosted={post.hasBeenPosted}
          />
        </div>
      ))}
    </div>
  );
}

export default Feed;
