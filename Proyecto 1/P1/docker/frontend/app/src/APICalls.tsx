import axios from "axios";
import { PostProps } from "./Home/Panels/Common/Post";
import { FriendProps } from "./Home/Panels/Common/Friend";
import { API_URL } from "./App";

interface StandardResponse {
  result: string;
}

interface FollowResponse {
  result: string;
  friends: number;
  doesFollow: boolean;
}

interface PromptResponse {
  id: string;
  title: string;
  artist: string;
  lyrics: string;
}

interface ProfileResponse {
  user: FriendProps;
  posts: PostProps[];
}

async function sendLogin(
  email: string,
  password: string
): Promise<StandardResponse> {
  const url = `${API_URL}/login`;
  try {
    const response = await axios.post(url, {
      email: email,
      password: password,
    });

    if (!response.data.user_id.toString()) {
      return { result: "error" };
    } else {
      localStorage.setItem("user_id", response.data.user_id.toString());
      localStorage.setItem("email", email);
      return response.data;
    }
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

async function sendRegister(
  name: string,
  username: string,
  email: string,
  password: string
): Promise<StandardResponse> {
  const url = `${API_URL}/register`;
  try {
    const response = await axios.post(url, {
      name: name,
      username: username,
      email: email,
      password: password,
    });

    if (!response.data.user_id.toString()) {
      return { result: "error" };
    } else {
      localStorage.setItem("user_id", response.data.user_id.toString());
      localStorage.setItem("email", email);
      return response.data;
    }
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

async function askPrompt(prompt: string): Promise<PromptResponse[]> {
  const url = `${API_URL}/prompt`;
  const response = await axios.post(url, { prompt: prompt });
  return response.data;
}

async function sendLike(post_id: string): Promise<StandardResponse> {
  const url = `${API_URL}/likeOrUnlike`;
  try {
    const response = await axios.post(url, {
      prompt_id: post_id,
      user_id: localStorage.getItem("user_id"),
    });

    return response.data;
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

async function sendPost(prompt: string): Promise<StandardResponse> {
  const url = `${API_URL}/postPrompt`;
  try {
    const response = await axios.post(url, {
      user_id: localStorage.getItem("user_id"),
      prompt: prompt,
    });

    if (response.data.result.toString() === "401") {
      return { result: "error" };
    } else {
      return { result: "success" };
    }
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

function mapPostToPostProps(posts: any): PostProps[] {
  return posts.map((post: any) => {
    return {
      PostID: post[0],
      PostUser: post[1],
      PostTime: post[4],
      PostPrompt: post[3],
      PostLikes: post[2],
      hasBeenPosted: true,
    };
  });
}

async function fillPostsWithAnswers(posts: PostProps[]): Promise<PostProps[]> {
  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const urlPrompt = `${API_URL}/prompt`;
    const responsePrompt = await axios.post(urlPrompt, {
      prompt: post.PostPrompt,
    });
    const urlLiked = `${API_URL}/hasLiked`;
    const responseLiked = await axios.post(urlLiked, {
      prompt_id: post.PostID,
      user_id: localStorage.getItem("user_id"),
    });
    posts[i].PostAnswer = responsePrompt.data;
    posts[i].hasUserLiked = responseLiked.data.hasLiked === 1 ? true : false;
  }

  return posts;
}

async function getFeedPosts(): Promise<PostProps[]> {
  const url = `${API_URL}/feed`;
  const response = await axios.post(url, {
    user_id: localStorage.getItem("user_id"),
  });
  const data = mapPostToPostProps(response.data.posts);
  return data;
}

async function getFeed(): Promise<PostProps[]> {
  const posts = await getFeedPosts();

  const postsWithAnswers = await fillPostsWithAnswers(posts);

  return postsWithAnswers;
}

async function search(query: string): Promise<PostProps[]> {
  const url = `${API_URL}/search`;
  const response = await axios.post(url, {
    query: query,
  });
  const posts = mapPostToPostProps(response.data.posts);

  const postsWithAnswers = await fillPostsWithAnswers(posts);

  return postsWithAnswers;
}

async function followUser(user_id: string): Promise<FollowResponse> {
  const url = `${API_URL}/followOrUnfollow`;
  try {
    const response = await axios.post(url, {
      user_id: localStorage.getItem("user_id"),
      friend_user_id: user_id,
    });

    return {
      result: response.data.result,
      friends: response.data.friends,
      doesFollow: response.data.doesFollow === 1 ? true : false,
    };
  } catch (error) {
    console.error(error);
    return { result: "error", friends: 0, doesFollow: false };
  }
}

function mapFriendToFriendProps(friends: any): FriendProps[] {
  return friends.map((friend: any) => {
    return {
      id: friend[0],
      name: friend[1],
      username: friend[2],
      bio: friend[3],
      friends: friend[4],
      isFriend: false,
    };
  });
}

async function checkFriendship(friends: FriendProps[]): Promise<FriendProps[]> {
  for (let i = 0; i < friends.length; i++) {
    const friend = friends[i];
    const url = `${API_URL}/isFriend`;
    const response = await axios.post(url, {
      user_id: localStorage.getItem("user_id"),
      friend_user_id: friend.id,
    });
    // ParseInt is necessary because the response might be a string
    friend.isFriend = response.data.doesFollow === 1 ? true : false;
  }

  return friends;
}

async function findFriends(findQuery: string): Promise<FriendProps[]> {
  const url = `${API_URL}/find`;
  const response = await axios.post(url, {
    query: findQuery,
  });

  const data = mapFriendToFriendProps(response.data.users);
  // Filter out user's own profile
  const filteredData = data.filter((friend) => {
    return friend.id.toString() !== localStorage.getItem("user_id");
  });

  const friends = await checkFriendship(filteredData);

  return friends;
}

async function getFriends(): Promise<FriendProps[]> {
  const url = `${API_URL}/friends`;
  const response = await axios.post(url, {
    user_id: localStorage.getItem("user_id"),
  });

  const data = mapFriendToFriendProps(response.data.profiles);
  const friends = await checkFriendship(data);

  return friends;
}

async function getProfile(): Promise<ProfileResponse> {
  const url = `${API_URL}/profile`;
  const response = await axios.post(url, {
    user_id: localStorage.getItem("user_id"),
  });

  const user = mapFriendToFriendProps(response.data.user)[0];
  user.isSelf = true;

  const posts = mapPostToPostProps(response.data.posts);
  const postsWithAnswers = await fillPostsWithAnswers(posts);

  return {
    user: user,
    posts: postsWithAnswers,
  };
}

async function deletePost(post_id: string): Promise<StandardResponse> {
  const url = `${API_URL}/deletePrompt`;
  try {
    const response = await axios.post(url, {
      prompt_id: post_id,
    });

    return response.data;
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

async function updateProfile(
  name: string,
  username: string,
  bio: string
): Promise<StandardResponse> {
  const url = `${API_URL}/updateProfile`;
  try {
    const response = await axios.post(url, {
      user_id: localStorage.getItem("user_id"),
      name: name,
      username: username,
      biography: bio,
    });

    return response.data;
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

async function updatePost(
  post_id: string,
  prompt: string
): Promise<StandardResponse> {
  const url = `${API_URL}/editPrompt`;
  try {
    const response = await axios.post(url, {
      prompt_id: post_id,
      prompt: prompt,
    });

    return response.data;
  } catch (error) {
    console.error(error);
    return { result: "error" };
  }
}

export type { PromptResponse };
export {
  sendLogin,
  sendRegister,
  askPrompt,
  sendLike,
  sendPost,
  getFeed,
  search,
  followUser,
  findFriends,
  getFriends,
  getProfile,
  deletePost,
  updateProfile,
  updatePost,
};
