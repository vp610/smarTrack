import './App.css';
import React, { useState, useEffect, createRef } from 'react';


function App() {
  const file = createRef();
  const onSubmit = async (e) => {
    e.preventDefault();
    const formD = new FormData();
    formD.set("video", file.current.value);
    try {
      const res = await fetch('/profile', {       // istead of /profile it has to match the url in FLASK to recieve the video
        method: "POST",
        body: formD
      });

      const parseRes = await res.json();
      if (parseRes.ok){
        alert("File has been uploaded");
      } else {
        console.error("Error in file upload");
      }

    } catch (e){
      console.error("An error has occured");
    }
  }

  const [data, setData] = useState([{}]) // used to fetch data from backend and manipulate it

  useEffect(() => {       // getting data of counts & then displayed in the return 
    fetch("/data").then(
      res => res.json()
    ).then (
        data => {
          setData(data)   // put the data from backend to the data var
          console.log(data) // remove it once you know data is being retrived
        }
    )
  }, [])

  return (
    <div className="App">
      <form onSubmit={onSubmit}>
        <input type="file" name="video" ref={file} />
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}

export default App;
