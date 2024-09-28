import { useState } from "react";
import { Button } from "react-bootstrap";
import "./Panels.css";
import Post from "./Common/Post";
import { ToastContainer, toast } from "react-toastify";
import { PromptResponse, askPrompt, sendPost } from "../../APICalls";

function Ask(): JSX.Element {
  const [hasAsked, setHasAsked] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState<PromptResponse[]>([]);

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

  return (
    <div className="panel">
      <ToastContainer position="top-right" />
      <h1>Ask PrompTunes</h1>
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
          onChange={(e) => setPrompt(e.target.value)}
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
              onClick={handlePost}
            >
              Post!
            </Button>
          </div>
        )}
      </form>
    </div>
  );
}

export default Ask;
