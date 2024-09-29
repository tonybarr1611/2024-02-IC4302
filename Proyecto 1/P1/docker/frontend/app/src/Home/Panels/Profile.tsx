import { useEffect, useState } from "react";
import Friend, { FriendProps } from "./Common/Friend";
import Post, { PostProps } from "./Common/Post";
import { getProfile } from "../../APICalls";

function Profile(): JSX.Element {
  const [profile, setProfile] = useState<FriendProps>();
  const [posts, setPosts] = useState<PostProps[]>();

  useEffect(() => {
    const fetchProfile = async () => {
      const response = await getProfile();
      setProfile(response.user);
      setPosts(response.posts);
    };
    fetchProfile();
  }, []);

  return (
    <div className="panel">
      <h1>Profile</h1>
      <p className="subtitles">Look at your profile</p>
      <div className="container">
        <div className="row">
          <div className="col mr-4 mb-5">
            {profile && (
              <Friend
                id={profile.id}
                name={profile.name}
                username={profile.username}
                bio={profile.bio}
                friends={profile.friends}
                isFriend={profile.isFriend}
                isSelf={profile.isSelf}
              />
            )}
          </div>
        </div>
      </div>
      <div className="container">
        <div className="row">
          <div className="col">
            <h2>Posts</h2>
            <p>Your own posts!</p>
            <div className="posts">
              {posts?.map((post) => (
                <Post
                  key={post.PostID}
                  PostID={post.PostID}
                  PostUser={post.PostUser}
                  PostTime={post.PostTime}
                  PostPrompt={post.PostPrompt}
                  PostAnswer={post.PostAnswer}
                  PostLikes={post.PostLikes}
                  hasBeenPosted={post.hasBeenPosted}
                  hasUserLiked={post.hasUserLiked}
                  isOwnPost={true}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
