import { useState } from "react";
import { Button } from "react-bootstrap";
import "./Panels.css";
import Post from "./Common/Post";
import { ToastContainer, toast } from "react-toastify";

function Ask(): JSX.Element {
  const [hasAsked, setHasAsked] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = () => {
    setHasAsked(true);
    const promptElement = document.getElementsByName(
      "prompt"
    )[0] as HTMLTextAreaElement;
    setPrompt(promptElement.value);
    setAnswer(
      "Taylor Swift - Who's afraid of little old me?\n … The whos who of Whos that? is poised for the attack\n But my bare hands paved their paths\n You dont get to tell me about sad\n … If you wanted me dead, you shouldve just said\n Nothing makes me feel more alive\n … So I leap from the gallows and I levitate down your street\n Crash the party like a record scratch as I scream\n Whos afraid of little old me?\n You should be\n … The scandal was contained\n The bullet had just grazed\n At all costs, keep your good name\n You dont get to tell me you feel bad\n … Is it a wonder I broke? Lets hear one more joke\n Then we could all just laugh until I cry\n … So I leap from the gallows and I levitate down your street\n Crash the party like a record scratch as I scream\n Whos afraid of little old me?\n I was tame, I was gentle til the circus life made me mean\n Dont you worry, folks, we took out all her teeth\n Whos afraid of little old me?\n Well, you should be\n … You should be\n (You should be) You should be\n You should be (you should be)\n You should be (you should be)\n You should be\n … So tell me everything is not about me\n But what if it is?\n Then say they didnt do it to hurt me\n But what if they did?\n … I wanna snarl and show you just how disturbed this has made me\n You wouldnt last an hour in the asylum where they raised me\n So all you kids can sneak into my house with all the cobwebs\n Im always drunk on my own tears, isnt that what they all said?\n That Ill sue you if you step on my lawn\n That Im fearsome and Im wretched and Im wrong\n Put narcotics into all of my songs\n And thats why youre still singing along\n … So I leap from the gallows and I levitate down your street\n Crash the party like a record scratch as I scream\n Whos afraid of little old me?\n I was tame, I was gentle til the circus life made me mean\n Dont you worry, folks, we took out all her teeth\n Whos afraid of little old me?\n Well, you should be\n … You should be\n (You should be) You should be\n Cause you lured me (you should be)\n And you hurt me (you should be)\n And you taught me\n … You caged me and then you called me crazy\n I am what I am cause you trained me\n So whos afraid of me?\n Whos afraid of little old me?\n Whos afraid of little old me?\n "
    );
  };

  const handlePost = () => {
    setHasAsked(false);
    setPrompt("");
    setAnswer("");
    toast.success("Posted successfully!");
  };

  return (
    <div className="askandsearch-panel">
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
