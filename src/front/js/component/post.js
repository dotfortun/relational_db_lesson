import React from "react";

const Post = ({ title, body, url, prev, next }) => {
  return (
    <div className="card" style={{ width: "100%" }}>
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-body">{body}</p>
      </div>
    </div>
  );
};

export default Post;
