import requests, base64, io, os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GETIMG_KEY")

apikey = key

#very good one, .04 per image
url = "https://api.getimg.ai/v1/essential-v2/text-to-image" 

# very cheap
#url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"


#url = "https://api.getimg.ai/v1/essential/text-to-image"

def generate(prompt,filename):
    filename = "temp/" + str(filename) + ".jpg"
    if url == "https://api.getimg.ai/v1/essential-v2/text-to-image":
        input_params = {
            "style" : "art",
            "prompt" : prompt,
            "output_format" : "jpeg",
            "width" : 1024,
            "height" : 1024,
            "steps" : 8,
            "guidance" : 20,
        }
    elif url == "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image":
        input_params = {
            "model" : "realvis-xl-v4",
            "prompt" : prompt,
            "output_format" : "jpeg",
            "width" : 512,
            "height" : 512,
            "steps" : 40,
            "guidance" : 20,
            "negative_prompt" : "cartoon"
        }
    elif url == "https://api.getimg.ai/v1/essential/text-to-image":
        input_params = {
            "prompt" : prompt,
            "output_format" : "jpeg",
            "width" : 1024,
            "height" : 1024,
            "steps" : 60,
            "guidance" : 1,
        }
    else: raise Exception("not real model")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": apikey
    }

    response = requests.post(url, headers=headers, json=input_params)
    decoded_img = base64.b64decode(response.json()["image"])
    img = Image.open(io.BytesIO(decoded_img))
    img.thumbnail((1080,1080), Image.LANCZOS)
    img.save(filename,'JPEG')

    return filename, response.json()["cost"]

def generateFrom(prompt, filename, savename):
    input_params = {
            "style" : "anime",
            "prompt" : prompt,
            "output_format" : "jpeg",
            "width" : 1024,
            "height" : 1024,
            "steps" : 60,
            "guidance" : 20,
            "strength": .5,
            "image" : str(base64.b64encode(open(filename, "rb").read()).decode('utf-8')),
            "seed" : 1
        }

    url = "https://api.getimg.ai/v1/stable-diffusion-xl/image-to-image"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": apikey
    }

    response = requests.post(url, headers=headers, json=input_params)
    print(response.json())
    decoded_img = base64.b64decode(response.json()["image"])
    img = Image.open(io.BytesIO(decoded_img))
    img.thumbnail((1080,1080), Image.LANCZOS)
    img.save(savename,'JPEG')
