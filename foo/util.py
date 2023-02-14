import ddddocr
import os

"""
识别验证码
"""


def ocr_code(file):
    ocr = ddddocr.DdddOcr()
    with open(file, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    os.remove(file)
    return res