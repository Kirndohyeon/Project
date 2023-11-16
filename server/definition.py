import io
import os
import warnings
import numpy as np
from PIL import Image
import torch
import cv2
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import openai
from segment_anything import sam_model_registry, SamPredictor
from googletrans import Translator

def stability_algorithm(image, sentence):
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

    os.environ['STABILITY_KEY'] = 'sk-S205IclhTAtN6Hsx1w3M61BvClNPRl4P6QKOKRLmxZeDqoef'
    
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'],
        verbose=True,
        engine="stable-diffusion-xl-beta-v2-2-2",  
    )
    
    image = Image.fromarray(image)

    new_width = image.width - (image.width % 64)
    new_height = image.height - (image.height % 64)
    input_image = image.resize((new_width, new_height))

    answers2 = stability_api.generate(
        prompt=sentence,
        init_image=input_image,
        start_schedule=0.5,
        seed=123467458,
        steps=30,
        cfg_scale=7.0,
        width=512,
        height=512,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    for resp in answers2:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                global img2
                img2 = Image.open(io.BytesIO(artifact.binary))
                img2.save("C:/Users/do150/Desktop/result/image-img2img.png")
    
    return 1

def openai_algo(content, page, character):
    openai.api_key = "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"

    cont = content + '를 한 페이지에 ' + character + '자 이내 한 문장으로, 페이지는 ' + page + '페이지, 한국어로 만들어줘'
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": cont}]
    )
    return completion['choices'][0]['message']['content']

def do_seg(image, sam, opt, x_in=None, y_in=None):

    predictor = SamPredictor(sam)

    predictor.set_image(image)

    if opt == 'Yes':
        x_in = image.shape[1] // 2
        y_in = image.shape[0] // 2
    
    elif opt == 'No':
        pass
    
    else:
        print("옵션 지정 오류")
        
    input_point = np.array([[x_in, y_in]])
    input_label = np.array([1])

    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )
    
    masked = masks.astype(np.uint8) * 255
    masked_image = cv2.bitwise_and(image, image, mask=masked[1])
    masked_image1 = cv2.bitwise_and(image, image, mask=masked[2])
    
    contours, _ = cv2.findContours(masked[1], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    contours1, _ = cv2.findContours(masked[2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x1, y1, w1, h1 = cv2.boundingRect(contours1[0])

    cropped_image = masked_image[y:y+h, x:x+w]
    cropped_image1 = masked_image1[y1:y1+h1, x1:x1+w1]
    
    return cropped_image, cropped_image1

def remove_grabcut_bg(image):
        tmp = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        r, g, b = cv2.split(image)
        rgba = [r,g,b,alpha]
        dst = cv2.merge(rgba,4)
        return dst

def translate_korean_to_english(text):
    translator = Translator()
    result = translator.translate(text, src='ko', dest='en')
    translated_text = result.text
    return translated_text
