import wave

class WaveGenerator(object):
    def __init__(self):
        pass

    def create_wav_file(wave_data, output_filename, sample_rate=8000, duration=1, frequency=440.0):
        num_frames = int(sample_rate * duration)

        # 创建 WAV 文件头
        with wave.open(output_filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # 单声道
            wav_file.setsampwidth(2)  # 16位样本宽度
            wav_file.setframerate(sample_rate)
            wav_file.setnframes(num_frames)
            wav_file.setcomptype('NONE', 'not compressed')
            wav_file.writeframes(wave_data.tobytes())
        return