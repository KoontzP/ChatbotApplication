import React, { useContext } from "react";

import { UserContext } from "../context/UserContext";

const Header = ({ title }) => {
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <div className="has-text-centered m-6" style={{ position: "relative" }}>
    {token && (
    <>
      <p className="subtitle">
        {title || "Welcome to the DialgoGPT chatbot, create a new message to talk to the chatbot"}
      </p>
      <button className="button" onClick={handleLogout} style={{ position: "absolute", top: "10px", right: "10px" }}>
        Logout
      </button>
    </>
  )}
</div>


  );
};

export default Header;