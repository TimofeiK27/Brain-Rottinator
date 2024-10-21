from diffusers import StableDiffusionPipeline
import torch

#generate image
def generate(prompt,filename):
    with torch.autocast(device):
        image = pipe(prompt + " , very cute, 4K",guidence_scale=10)["images"][0]
    image.save("temp/" + str(filename) + '.png')
    return "temp/" + str(filename) + '.png', 0

modelid = "runwayml/stable-diffusion-v1-5"
#modelid = "CompVis/stable-diffusion-v1-4"
#pipe = StableDiffusionPipeline.from_pretrained(modelid,revision="fp16",torch_dtype=torch.float16)
pipe = StableDiffusionPipeline.from_pretrained(modelid,torch_dtype=torch.float16,safety_checker=None,use_safetensors=True)

device="cuda"
pipe.to(device)
