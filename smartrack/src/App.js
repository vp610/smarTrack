import './App.css';
import React, { useState, useEffect} from 'react';


function App() {
  const onSubmit = async (e) => {
    e.preventDefault();
  
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
      <form method='POST' enctype='multipart/form-data' onSubmit={onSubmit}>
        <input type="file" name="video" accept="video/mp4" />
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}

export default App;
