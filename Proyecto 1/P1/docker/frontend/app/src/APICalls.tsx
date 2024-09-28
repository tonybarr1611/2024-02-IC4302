import axios from "axios";
import { PostProps } from "./Home/Panels/Common/Post";
import { API_URL } from "./App";

interface StandardResponse {
  result: string;
}

interface PromptResponse {
  id: string;
  title: string;
  artist: string;
  lyrics: string;
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

export type { PromptResponse };
export {
  sendLogin,
  sendRegister,
  askPrompt,
  sendLike,
  sendPost,
  getFeed,
  search,
};
