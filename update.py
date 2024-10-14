import requests
from bs4 import BeautifulSoup
import os
import zipfile
import shutil


def get_repository_info(repo_url):
    response = requests.get(repo_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取仓库名称
    repo_name = soup.find('strong', class_='mr-2').a.text.strip()

    # 获取最新发布版本的下载链接
    latest_release = soup.find(
        'a', class_='muted-link').get('href') if soup.find('a', class_='muted-link') else None

    return {
        'name': repo_name,
        'latest_release': latest_release
    }


def download_latest_release(repo_url, download_path):
    # 获取最新发布版本的 zip 下载链接
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"  # 假设使用主分支
    response = requests.get(zip_url)

    with open(download_path, 'wb') as f:
        f.write(response.content)


def update_repository(local_path, download_path):
    # 删除旧版本
    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    # 解压新版本
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(local_path))

    # 重命名文件夹
    os.rename(os.path.join(os.path.dirname(
        local_path), 'xiaomo-main'), local_path)


def main():
    repo_url = 'https://github.com/lldxlzy/xiaomo'  # 指定要爬取的仓库
    local_path = 'xiaomo'  # 本地存储路径
    download_path = 'latest_release.zip'  # 下载的 zip 文件名

    repo_info = get_repository_info(repo_url)

    if repo_info['latest_release']:
        print(f"发现更新，正在下载最新版本...")
        download_latest_release(repo_url, download_path)
        print(f"下载完成，正在更新本地仓库...")
        update_repository(local_path, download_path)
        print("更新完成！")
    else:
        print("没有可用的更新。")


main()