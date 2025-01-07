import React, { useState } from "react";

const ChatModal = ({ active, handleModal, token, setErrorMessage }) => {
  const [content, setContent] = useState("");
  const [chatbotResponse, setChatbotResponse] = useState("");



  const handleCreateMessages = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        content, // Send only the user's message
      }),
    };
    const response = await fetch("/api/messages", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong when sending the message");
    } else {
      const data = await response.json();
      setChatbotResponse(data.bot_response); // Set the chatbot's response
    }
  };

  return (
    <div className={`modal ${active && "is-active"}`}>
      <div className="modal-background" onClick={handleModal}></div>
      <div className="modal-card">
        <header className="modal-card-head has-background-info-dark">
          <h1 className="modal-card-title">DialgoGPT chatbot</h1>
        </header>
        <section className="modal-card-body">
          <form onSubmit={handleCreateMessages}>
            <div className="field">
              <label className="label">Your Message</label>
              <div className="control">
                <input
                  type="text"
                  placeholder="Enter your message"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  className="input"
                  required
                />
              </div>
            </div>
            <div className="field">
              <label className="label">Chatbot Response</label>
              <div className="control">
                <textarea
                  readOnly
                  value={chatbotResponse}
                  className="textarea"
                ></textarea>
              </div>
            </div>
            <button type="submit" className="button is-primary">
              Send
            </button>
            <button type="button" className="button" onClick={handleModal}>
              Cancel
            </button>
          </form>
        </section>
      </div>
    </div>
  );
};

export default ChatModal;
