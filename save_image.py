import requests
from PIL import Image
import io

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

# Example usage:
# s3_url = "https://aeye-docs.s3.amazonaws.com/Image+(7).jpeg"
# local_path = s3_url.split('/')
# download_s3_image_without_boto3(s3_url, local_path[-1])

import requests
import io
from PIL import Image
import numpy as np
from inference import nparray_to_caption, img_to_caption


def s3_image_to_numpy_without_boto3(url):

  response = requests.get(url, stream=True)
  response.raise_for_status()
  img_data = response.content
  image_file = io.BytesIO(img_data)
  img = Image.open(image_file)
  np_array = np.array(img)

#   pil_image = img.copy()


  return np_array


url = "https://aeye-docs.s3.amazonaws.com/Image+(7).jpeg"
# resp = s3_image_to_numpy_without_boto3(url=url)
# print(resp)

# image_data = s3_image_to_numpy_without_boto3(url)
# print(image_data)
# response = nparray_to_caption(image_data)
# print(response)

# response = img_to_caption(["image.jpeg"])
# print(response)



# Docker commands
# -> docker build -t image_model . 

# -> docker run -p 9000:8080 image_model

# Parallel(To test above command)
# -> curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"file":"hospitals/common_files/emergency.jpg"}'


# -> aws ecr get-login-password --region <Region> | docker login --username AWS --password-stdin <Account-ID>.dkr.ecr.<Region>.amazonaws.com

# -> aws ecr create-repository --repository-name demo-lambda --image-scanning-configuration scanOnPush=true