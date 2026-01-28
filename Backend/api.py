from google import genai
from google.genai import types

client = genai.Client(api_key = "AIzaSyB8BzuHboQleEbQeymkN3KI51uDcbCl2Q0")


def gemini_call(video_url:str):
  yt = types.Part(
    file_data = types.FileData(
      file_uri=video_url,
      mime_type = "video/mp4"
    )
  )


  response = client.models.generate_content(
    model = "gemini-3-flash-preview",
    contents = [yt , "please summarise this in crisp"],
  )
  return response.text


# print(response.text)