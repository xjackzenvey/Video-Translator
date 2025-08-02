import requests
import loguru
import time

class AppWorldsAPITranslator:
    
    @staticmethod
    def translate(ja_text: str):
        '''
        ### 使用 AppWorlds 免费 API 进行翻译，最多2s1次
        :param ja_text: 日语文本
        '''
        
        time.sleep(1.3)  # 避免请求过快
        
        req_url = f'https://translate.appworlds.cn?text={ja_text}&from=ja&to=zh-CN'
        
        try:
            resp = requests.get(req_url)
            json_data = resp.json()
            assert json_data['code'] == 200, f"Request Code got {json_data['code']} and message {json_data['msg']}"
            
            return json_data['data']
        
        except Exception as e:
            loguru.logger.error(str(e))
            
            
        