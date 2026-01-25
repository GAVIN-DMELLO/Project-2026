import {useState} from 'react'
import axios from 'axios'

function Test(){

let[set , setData] = useState("Loading....");


  const call = async () =>{
  try{
    const response = await axios.get("http://127.0.0.1:8000/");
    setData(response.data.message);
  }
  catch(error){
    console.error(error);
  }
};

  console.log(set);

  return (
    <>
      <button onClick={call}>Click</button>
      <h2>
        {set}
      </h2>
    </>
  )
}


export default Test;