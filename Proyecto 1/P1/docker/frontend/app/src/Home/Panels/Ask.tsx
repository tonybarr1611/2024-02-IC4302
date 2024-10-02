import { useEffect, useState } from "react";
import { Button } from "react-bootstrap";
import "./Panels.css";
import Post from "./Common/Post";
import { ToastContainer, toast } from "react-toastify";
import {
  PromptResponse,
  askPrompt,
  sendPost,
  updatePost,
} from "../../APICalls";

interface AskProps {
  id?: string;
  curr_prompt?: string;
}

function Ask({ id, curr_prompt }: AskProps): JSX.Element {
  const [hasAsked, setHasAsked] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState<PromptResponse[]>([]);

  useEffect(() => {
    if (id && curr_prompt) {
      setHasAsked(true);
      setPrompt(curr_prompt);
    }
  }, []);

  const handleAsk = async () => {
    setHasAsked(true);
    const promptElement = document.getElementsByName(
      "prompt"
    )[0] as HTMLTextAreaElement;
    setPrompt(promptElement.value);

    const response = await askPrompt(promptElement.value);

    setAnswer(response);
  };

  const handlePost = async () => {
    const response = await sendPost(prompt);
    if (response.result === "error") {
      toast.error("Post failed", {
        autoClose: 1500,
        theme: "colored",
      });
    } else {
      toast.success("Posted successfully!");
      setHasAsked(false);
      setPrompt("");
      setAnswer([
        { id: "", title: "string", artist: "string", lyrics: "string" },
      ]);
    }
  };

  const handleUpdate = async () => {
    const response = await updatePost(id || "", prompt);
    if (response.result === "error") {
      toast.error("Update failed", {
        autoClose: 1500,
        theme: "colored",
      });
    } else {
      toast.success("Updated successfully!");
      window.location.assign("/home/profile");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(e.target.value);
    setHasAsked(false);
  };

  return (
    <div className="panel">
      <ToastContainer position="top-right" />
      {id && curr_prompt ? <h1>Edit your prompt</h1> : <h1>Ask PrompTunes</h1>}
      <p className="subtitles">We will give you a song based on your needs!</p>
      <form className="width-full">
        <label className="mt-4">
          <p>Your prompt goes here!</p>
        </label>
        <textarea
          name="prompt"
          placeholder="Type your prompt here"
          cols={30}
          rows={3}
          className="ask-input"
          value={prompt}
          onChange={handleChange}
        />
        <Button variant="primary" className="w-100 mb-3" onClick={handleAsk}>
          Ask!
        </Button>
        {hasAsked && (
          <div>
            <Post
              PostUser="PrompTunes"
              PostTime="Now"
              PostPrompt={prompt}
              PostAnswer={answer}
              PostLikes={0}
              hasBeenPosted={false}
            />
            <Button
              variant="primary"
              className="w-100 mb-3"
              onClick={id ? handleUpdate : handlePost}
            >
              Post!
            </Button>
          </div>
        )}
      </form>
    </div>
  );
}

export type { AskProps };

export default Ask;
