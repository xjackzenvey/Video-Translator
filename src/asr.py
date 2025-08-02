from funasr import AutoModel as ASRAutoModel

class ASREngine:
    def __init__(self, model_path: str, device: str, **kwargs):
        '''
        ### 初始化 ASR 引擎
        :param model_path: 模型路径
        :param device: 设备类型 ('cpu' or'cuda')
        '''
        
        self.model = ASRAutoModel(
            model=model_path,
            device=device,
            disable_update=True,
            **kwargs
        )
        
        
    def recognize(self, audio_path: str) -> str:
        res = self.model.generate(audio_path)
        cleaned = ''.join(res[0]['text'].split())
        return cleaned