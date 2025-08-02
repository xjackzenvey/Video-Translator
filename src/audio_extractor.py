import moviepy
import tempfile


class BaseAudioExtractor:
    
    @staticmethod
    def extract(video_path: str = None, v_clip: moviepy.VideoFileClip = None, start_time: float = None, end_time: float = None, save_audio_path = None) -> str:
        '''
        ### 提取视频中的一段音频
        :param video_path:      视频文件的路径
        :param start_time:      开始时间（秒）,默认为视频开头；
        :param end_time:        结束时间（秒）,默认为视频结尾；
        :param save_audio_path: 保存音频的路径。如果为 None，存储为 tempfile
        '''
        
        assert (video_path or v_clip) and not (video_path and v_clip), "请提供视频文件路径或 moviepy.VideoFileClip 对象，但不能同时提供两者。"
        
        if v_clip is None:
            v_clip = moviepy.VideoFileClip(video_path)
            
        v_dur = v_clip.duration
        
        if start_time is None:
            start_time = 0
            
        if end_time is None:
            end_time = v_dur
            
        assert 0 <= start_time < end_time <= v_dur, "时间范围不合法。"
        
        audio_clip = v_clip.audio.subclipped(start_time, end_time)
        
        if save_audio_path is None:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                save_audio_path = temp_file.name
                
        audio_clip.write_audiofile(save_audio_path, codec='mp3')
        
        return save_audio_path
        