import os
from pathlib import Path
import subprocess


class FileUtils:

    @staticmethod
    def get_project_dir():
        # 工具类的上一层级就是项目根目录
        FILE = Path(__file__).parent.resolve()
        project_dir = os.path.dirname(FILE)
        return project_dir

    @staticmethod
    def create_dir(dir_path: str):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def delete_file(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def video_merge_audio(video_path: str, audio_path: str,
                          merge_file_path: str):
        video_audio_merge_cmd = f'ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -strict experimental {merge_file_path}'
        subprocess.run(video_audio_merge_cmd, shell=True)
