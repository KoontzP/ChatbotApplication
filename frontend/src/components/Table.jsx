import React, { useContext, useState } from "react";
import moment from "moment";

import ErrorMessage from "./ErrorMessage";
import ChatModal from "./ChatModal";
import { UserContext } from "../context/UserContext";

const Table = () => {
  const [token] = useContext(UserContext);
  const [messages, setMessages] = useState([]); // Renamed from `chat` to `messages`
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);

  const getMessages = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await fetch("/api/messages", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the chat messages");
    } else {
      const data = await response.json();
      setMessages(data);
      setLoaded(true);
    }
  };


  const handleDelete = async (id) => {
    const requestOptions = {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await fetch(`/api/messages/${id}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Failed to delete chat message");
    }
    getMessages();
  };

  const handleModal = () => {
    setActiveModal(!activeModal);
    getMessages(); // Refresh messages after modal is closed
  };



  return (
    <>
      <ChatModal
        active={activeModal}
        handleModal={handleModal}
        token={token}
        setErrorMessage={setErrorMessage}
      />
      <button
        className="button is-fullwidth mb-5 is-primary"
        onClick={() => setActiveModal(true)}
      >
        Create Chat
      </button>
      <ErrorMessage message={errorMessage} />
      {loaded && messages.length ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
              <th>Content</th>
              <th>Bot Response</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {messages.map((message) => (
              <tr key={message.id}>
                <td>{message.user_message}</td>
                <td>{message.bot_response}</td>
                <td>{moment(message.date_created).format("MMM Do YY")}</td>
                <td>
                  <button
                    className="button mr-2 is-danger is-light"
                    onClick={() => handleDelete(message.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>{loaded ? "No messages available" : "Loading..."}</p>
      )}
    </>
  );
};

export default Table;
