from dotenv import load_dotenv
from imagekitio import ImageKit
import os

#this function look for the presence of .env, and load the values in so we can access them
load_dotenv()

imagekit = ImageKit(
    #to access those value, we use os.getenv
    private_key = os.getenv("IMAGEKIT_PRIVATE_KEY"),
    public_key = os.getenv("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint = os.getenv("IMAGEKIT_URL")
)