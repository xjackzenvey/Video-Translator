from .asr import ASREngine
from .audio_extractor import BaseAudioExtractor as AudioExtractor
from .translate import AppWorldsAPITranslator as Translator
import moviepy


class ProcessWorkFlow:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.video_clip = moviepy.VideoFileClip(video_path)
        self.video_fps = self.video_clip.fps
        self.video_duration = self.video_clip.duration
        
        self.rec_txt = ""
        self.translated_txt = ""
        
    def run_workflow(self, AudioExtractor=AudioExtractor, ASREngine=ASREngine, Translator=Translator, progress_callback=None):
        '''
        ### 运行 workflow
        :param AudioExtractor: 音频提取器类
        :param ASREngine: ASR 引擎类的实例
        :param Translator: 翻译器类
        :param progress_callback: 进度回调函数，接收两个参数：进度百分比和状态信息
        '''
        
        audio_path = AudioExtractor.extract(v_clip=self.video_clip)
        if progress_callback:
            progress_callback(10, '音频提取完成')
            
        rec_txt = ASREngine.recognize(audio_path)
        if progress_callback:
            progress_callback(50, '语音识别完成')
            
        translated_txt = Translator.translate(rec_txt)
        if progress_callback:
            progress_callback(100, '翻译完成')
            
        print(f"原文: {rec_txt}")
        print(f"翻译: {translated_txt}")
        
        return rec_txt, translated_txt
    


    
    
if __name__ == "__main__":
    video_path = 'examples/test.mp4'
    ProcessWorkFlow(video_path).run_workflow()