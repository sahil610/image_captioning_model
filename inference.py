import utils
import torch
from pathlib import Path
import requests
from models.blip import blip_decoder
# from .models import blip

from tqdm import tqdm
import argparse
import numpy as np
from PIL import Image


def init_parser(**parser_kwargs):
    """
    This function initializes the parser and adds arguments to it
    :return: The parser object is being returned.
    """
    parser = argparse.ArgumentParser(description="Image caption CLI")
    parser.add_argument("-i", "--input", help="Input directoryt path, such as ./images")
    parser.add_argument("-b", "--batch", help="Batch size", default=1, type=int)
    parser.add_argument(
        "-p", "--paths", help="A any.txt files contains all image paths."
    )
    parser.add_argument(
        "-g",
        "--gpu-id",
        type=int,
        default=0,
        help="gpu device to use (default=None) can be 0,1,2 for multi-gpu",
    )

    return parser


def init_model():
    """
    > Loads the model from the checkpoint file and sets it to eval mode
    :return: The model is being returned.
    """

    print("Checkpoint loading...")
    model = blip_decoder(
        pretrained="./checkpoints/model_large_caption.pth", image_size=384, vit="large"
    )
    model.eval()
    model = model.to(device)
    print(f"\nModel to {device}")
    return model


parser = init_parser()
opt = parser.parse_args()

device = torch.device(f"cuda:{opt.gpu_id}" if torch.cuda.is_available() else "cpu")
print(f'Device: {device}')

if not Path("checkpoints").is_dir():
    print(f"checkpoint directory did not found.")
    utils.create_dir("checkpoints")

if not Path("checkpoints/model_large_caption.pth").is_file():
    utils.download_checkpoint()

model = init_model()


def img_to_caption(batch):
    with torch.no_grad():
        print("Inference started")
        # batch = ["images/image_002.png"]
        pil_images = utils.read_with_pil(batch)
        # print(pil_images)
        transformed_images = utils.prep_images(pil_images, device)
        # print(transformed_images)
        if not Path("captions").is_dir():
            print(f"captions directory did not found.")
            utils.create_dir("captions")
                
        with open(f"captions/normal_captions.txt", "w+") as file:
            for path, image in zip(batch, transformed_images):


                caption = model.generate(
                    image, sample=False, num_beams=1, max_length=20, min_length=5
                )
                print(caption)
                file.write(path + ", " + caption[0] + "\n")
        return caption[0]
    

def download_s3_image_without_boto3(s3_url, local_path):
  """Downloads an S3 image to a local path without using boto3.

  Args:
      s3_url: The URL of the S3 object.
      local_path: The local path to save the image.
  """
  response = requests.get(s3_url, stream=True)
  response.raise_for_status()

  with open(local_path, 'wb') as f:
      for chunk in response.iter_content(1024):
          f.write(chunk)