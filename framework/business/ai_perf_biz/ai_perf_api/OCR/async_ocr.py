#async_ocr.py
# http异步请求

import json
import sys
sys.path.append("..")
import framework.utils.image_utils as comAPI
import framework.core.concurrent.cwAsyncRequests as http

class ocr(http.cwRequests):
    #异步请求
    async def read(self, url, image_file):
        dict = {'img': ''}
        img_data = comAPI.read_image(image_file)
        if img_data == None:
            return "read_image error"

        dict['img'] = comAPI.base64_encode(img_data)
        dict['imgID'] = image_file
        json_str = json.dumps(dict)
        return await self.get(url, json_str)