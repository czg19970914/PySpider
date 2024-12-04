from requests import Response
from tqdm import tqdm


class DownloadUtils:

    @staticmethod
    def download_file(save_file_path: str, file_response: Response,
                      bar_description: str):
        # 获取文件总大小，用于设置进度条
        total_size = int(file_response.headers.get('content-length', 0))
        download_bar = tqdm(total=total_size)
        with open(save_file_path, mode='wb') as f:
            # 把视频分成 1024 * 1024 * 2 为等分的大小 进行遍历
            for file_chunk in file_response.iter_content(1024 * 1024 * 2):
                f.write(file_chunk)
                # 更新进度条
                download_bar.set_description(bar_description)
                # 更新进度条长度
                download_bar.update(1024 * 1024 * 2)
        download_bar.set_description('下载完成！')
        download_bar.clear()
