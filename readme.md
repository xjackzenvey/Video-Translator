

# Video-Translator 视频翻译工具

剪视频的时候写的，用于将视频片段中的日语声音转换为文字，并翻译为中文。

欢迎提出 issue 或 [与我联系](mailto://xjackzenvey@outlook.com)！
 

### 部署

```
# 安装 Python 依赖包

# CPU 版本
pip install -r requirements.txt  

# GPU 版本
pip install -r requirements-gpu.txt  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


# 使用 modelscope 下载 日语ASR 模型
modelscope download --model iic/speech_UniASR_asr_2pass-ja-16k-common-vocab93-tensorflow1-offline --local_dir models/asr_model

# 启动
python launch.py

```

### 使用到的框架

- [ttkbootstrap 用于界面美化](https://github.com/israel-dryer/ttkbootstrap)
- [appworlds 提供的免费翻译 API](https://appworlds.cn/translate/)
- [moviepy 用于视频处理](https://github.com/Zulko/moviepy)



### 作者

xjackzenvey@outlook.com

BiliBili: [白色鱼鱼喵](https://space.bilibili.com/3546793577024347)


