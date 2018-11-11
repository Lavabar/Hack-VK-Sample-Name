#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

import requests
from io import BytesIO

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ubuntu/hackVK/grobot-ede0797ed7ff.json"

from translit_v1 import transliterate

with open("composers_eng.txt", "r") as f:
    composers_eng = [line.replace("\n", "") for line in f]
with open("composers_rus.txt", "r") as f:
    composers_rus = [line.replace("\n", "") for line in f]

def add_composer(rus_name):
    composers_rus.append(rus_name)
    composers_eng.append(transliterate(rus_name))
    with open("composers_eng.txt", "w") as f:
        for comp in composers_eng:
            f.write(comp + "\n")
    with open("composers_rus.txt", "w") as f:
        for comp in composers_rus:
            f.write(comp + "\n")

def del_composer(rus_name):
    idx = composers_rus.index(rus_name)
    composers_rus.pop(idx)
    composers_eng.pop(idx)
    with open("composers_eng.txt", "w") as f:
        for comp in composers_eng:
            f.write(comp + "\n")
    with open("composers_rus.txt", "w") as f:
        for comp in composers_rus:
            f.write(comp + "\n")


def report(annotations):
    """Prints detected features in the provided web annotations."""
    # [START vision_web_detection_tutorial_print_annotations]
    if annotations.web_entities:
        ents = annotations.web_entities[:3]
        for ent in ents:
            for word in str(ent.description).split():
                if word in composers_eng:
                    idx = composers_eng.index(word)
                    return composers_rus[idx]
    return "noname"
    # [END vision_web_detection_tutorial_print_annotations]

def detect_faces(image, path):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()
    response = client.face_detection(image=image)
    faces = response.face_annotations

    for face in faces:
        vertices = ([(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])
        if path.startswith('https'):
            response = requests.get(path)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(path)
        
        im2 = image.crop([vertices[0][0], vertices[0][1],
                  vertices[2][0] - 1, vertices[2][1] - 1])
        im2.save('output-crop.jpg', 'JPEG')

def get_name(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('https') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
    detect_faces(image, path)
    with io.open("output-crop.jpg", 'rb') as image_file:
        content = image_file.read()
        fc_img = types.Image(content=content)
    web_detection = client.web_detection(image=fc_img).web_detection

    return report(web_detection)


if __name__ == '__main__':
    url = "https://pp.userapi.com/c851132/v851132402/42a26/dCKwCsVQibs.jpg"
    #url = "example.jpg"
    name = get_name(url)

    print(name)
