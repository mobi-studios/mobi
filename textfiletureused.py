import requests
import zipfile
import os
import logging

def setup_logging():
    logging.basicConfig(
        filename='error.log',  # 日志文件名
        level=logging.ERROR,    # 只记录错误及以上级别的日志
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
def main():
    setup_logging()

    def download_file(url, destination):
        """下载文件"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(destination, 'wb') as file:
                file.write(response.content)
            print(f"成功下载文件：{destination}")
        except requests.exceptions.RequestException as e:
            print(f"下载失败：{e}")

    def unzip_file(zip_path, extract_to):
        """解压文件"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"成功解压文件：{zip_path} 到 {extract_to}")
        except zipfile.BadZipFile:
            print(f"解压失败：{zip_path} 不是一个有效的 ZIP 文件")

    def compare_files(file1_path, file2_path):
        """比较两个文件的内容"""
        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
                file1_lines = file1.readlines()
                file2_lines = file2.readlines()

            max_lines = max(len(file1_lines), len(file2_lines))
            for i in range(max_lines):
                line1 = file1_lines[i].strip() if i < len(file1_lines) else "[未定义]"
                line2 = file2_lines[i].strip() if i < len(file2_lines) else "[未定义]"

                if line1 != line2:
                    print(f"第 {i + 1} 行不一致:\n文件1: {line1}\n文件2: {line2}")
                else:
                    print(f"第 {i + 1} 行一致: {line1}")

        except FileNotFoundError as e:
            print(f"错误：未找到文件 - {e.filename}")
        except Exception as e:
            print(f"发生错误：{e}")

    url = 'https://github.com/lldxlzy/xiaomo/releases/download/textfileture/textfiletureused.zip'  # 实际 URL
    destination = 'downloaded_file.zip'
    extract_to = 'extracted_files'

    os.makedirs(extract_to, exist_ok=True)

    # 下载文件
    download_file(url, destination)

    # 解压文件
    unzip_file(destination, extract_to)

    # 比较的两个文件路径
    file1_path = os.path.join("cheak(don't use!!!).txt")  # 确保路径正确
    file2_path = os.path.join(extract_to, "cheak(don't use!!!).txt")  # 确保路径正确

    # 比较文件
    compare_files(file1_path, file2_path)

    print("处理完成。")
