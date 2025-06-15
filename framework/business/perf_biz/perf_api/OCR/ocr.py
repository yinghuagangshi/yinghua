# read ocr class
# author:shilingang
# http同步请求方式

import json

import sys
sys.path.append("..")
import common.common as comAPI
import framework.core.concurrent.cwRequests as httpRequests

#继承同步base http request
class ocr(httpRequests.cwRequests):
    def read(self, url, image_file):
        dict = {'img': ''}
        json_headers = {'content-type': "application/json"}

        img_data = comAPI.read_image(image_file)
        if img_data == None:            
            return None

        dict['img'] = comAPI.base64_encode(img_data)
   
        json_str = json.dumps(dict)

        return self.get(url, json_str, json_headers)


# for test
if __name__ == '__main__':
    ocr = ocr()
    bRet = ocr.read("http://10.128.162.176:32345/ocr/idcard", "d:\\id.jpg")
    print(bRet)
    if bRet:
        print(" 识别结果:" + str(ocr.get_data() ))
    else:
        print(" 请求错误: " + str(ocr.get_error()))