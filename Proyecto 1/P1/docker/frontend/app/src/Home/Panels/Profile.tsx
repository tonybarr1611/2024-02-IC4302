import Friend from "./Common/Friend";

function Profile(): JSX.Element {
  return (
    <div className="panel">
      <h1>Profile</h1>
      <p className="subtitles">Look at your profile</p>
      <div className="container">
        <div className="row">
          <div className="col mr-4 mb-5">
            <Friend
              name="Myself"
              username="MeUser"
              bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
              friends={8}
              isFriend={false}
              isSelf={true}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
