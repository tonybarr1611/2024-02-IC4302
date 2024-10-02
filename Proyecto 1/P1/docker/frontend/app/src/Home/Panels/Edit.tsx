import { useLocation } from "react-router-dom";
import Ask, { AskProps } from "./Ask";

function Edit(): JSX.Element {
  const location = useLocation();
  const { id, curr_prompt }: AskProps = location.state || {};

  return (
    <>
      <Ask id={id} curr_prompt={curr_prompt} />
    </>
  );
}

export default Edit;
