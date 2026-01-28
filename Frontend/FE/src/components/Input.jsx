import {useState} from "react"
import axios from "axios"

function Input(){

  const[url , setUrl] = useState("");
  const[resp , updateResp] = useState("");

  const callBackendAPI = async (url) => {
    try{
      const response = await axios.post("http://127.0.0.1:8000/summarise" , {youtubeurl : url});
      updateResp(response.data.summary);
    }
    catch(error){
      console.error(error);
    }
  
  }


  return (
    <>
      <input type="text" value={url} onChange={(e) => setUrl(e.target.value)}/>
      <button className="summarise-butn" onClick={()=> callBackendAPI(url)}>Summarise</button>
      <h2>{resp}</h2>
    </>
  )
}

export default Input;