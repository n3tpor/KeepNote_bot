from openai import OpenAI

class AI_INTERACTION():
    def __init__(self,openAiKey):
        self.client = OpenAI(api_key=openAiKey)
    def textToNote(self,text):
      return self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "assistant", "content":"You are a service that takes unstructured text as input and outputs a JSON structure. A valid output will contain one field named named 'content'. The 'content' field will be a list of items each represented with a string that MUST contain an emoji that MUST ACCURATLEY REPRESENT THE ITEM and the name of the item, the emoji MUST BE PART OF THE OFFICIAL UNICODE CHARACTER DATABASE. All items from the original list provided in plain text MUST be included in the new list, items MUST NOT BE REMOVED. The response MUST BE JSON, do not reply anything else."},
          {"role": "user", "content": f"{text}"}
        ],
        temperature=0
      ).choices[0].message.content
    def audioToText(self,filePath):
      audio_file = open(f"{filePath}", "rb")
      return self.client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file, 
      response_format="text"
      )
    def imageToText(self,url):
      return self.client.chat.completions.create(
      model="gpt-4-vision-preview",
        messages=[
          {
            "role": "user",
            "content": [
              {"type": "text", "text": "Extract all the test in this image, only include the raw text, no formatting or explanation"},
              {
                "type": "image_url",
                "image_url": {
                "url": f"{url}",
                },
              },
            ],
          }
        ],
        max_tokens=300,
      ).choices[0].message.content

