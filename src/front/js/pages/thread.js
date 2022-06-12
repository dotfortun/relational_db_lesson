import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import Post from "../component/post";

const Thread = () => {
  const { store, actions } = useContext(Context);

  useEffect(() => {
    actions.getThread();
  });

  return (
    <div className="container">
      <div className="row">
        <div className="col col-6 offset-3 d-flex flex-column">
          {store.thread.map((elem, idx) => {
            return <Post key={idx} title={elem.title} body={elem.body} />;
          })}
        </div>
      </div>
    </div>
  );
};

export default Thread;
