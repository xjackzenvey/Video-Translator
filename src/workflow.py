from .asr import ASREngine
from .audio_extractor import BaseAudioExtractor as AudioExtractor
from .translate import AppWorldsAPITranslator as Translator


def workflow(video_path):
    audio_path = AudioExtractor.extract(video_path)
    asr_eng = ASREngine(model_path='models/asr_model', device='cuda')
    rec_txt = asr_eng.recognize(audio_path)
    translated_txt = Translator.translate(rec_txt)
    
    print(f"原文: {rec_txt}")
    print(f"翻译: {translated_txt}")
    
    return rec_txt, translated_txt
    
    
if __name__ == "__main__":
    video_path = 'examples/test.mp4'
    workflow(video_path)