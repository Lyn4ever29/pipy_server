import json
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import subprocess
from libpip2pi.commands import dir2pi

class SyncPypi:
    def __init__(self, config_file='config.json'):
        """
        从 YAML 配置文件初始化 PipDownloadConfig 对象。

        Args:
        - config_file (str): YAML 配置文件的路径。
        """
        with open(config_file, 'r') as f:
            config = json.load(f)

        # 必需参数
        self.requirements_file = config.get('requirements_file', 'requirements.txt')
        self.download_path = config.get('download_path', '/path/to/save/packages')

        # 可选参数
        self.index_urls = config.get('index_urls', ['https://pypi.org/simple/'])
        self.platforms = config.get('platforms', ['manylinux1_x86_64'])
        self.python_versions = config.get('python_versions', ['3.7'])

        self.implementation = config.get('implementation', None)
        self.abi = config.get('abi', None)
        self.find_links = config.get('find_links', [])
        self.timeout = config.get('timeout', 60)
        self.retries = config.get('retries', 3)
        self.trusted_hosts = config.get('trusted_hosts', [])
        self.no_deps = config.get('no_deps', False)
        self.no_binary = config.get('no_binary', [])
        self.only_binary = config.get('only_binary', [])
        self.prefer_binary = config.get('prefer_binary', False)
        self.pre = config.get('pre', False)
        self.no_cache_dir = config.get('no_cache_dir', False)
        self.no_build_isolation = config.get('no_build_isolation', False)
        self.constraint_file = config.get('constraint_file', None)

    def execute_pip_download(self):
        """
        对指定文件中的每个依赖进行 pip download。
        """

        # 检查下载路径是否存在，不存在则创建
        os.makedirs(self.download_path, exist_ok=True)

        with open(self.requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 构建子目录名称（使用依赖包名）
                package_name = line.split()[0].strip()
                # subdirectory = os.path.join(os.getcwd(), package_name)
                # os.makedirs(subdirectory, exist_ok=True)

                # 构建命令
                for platform in self.platforms:
                    for python_version in self.python_versions:
                        cmd = ['pip', 'download',
                               '-d', self.download_path,
                               package_name,
                               '--timeout', str(self.timeout),
                               '--retries', str(self.retries)]

                        for index_url in self.index_urls:
                            cmd.extend(['--index-url', index_url])
                        if self.platforms:
                            cmd.extend(['--platform', platform])
                        if self.python_versions:
                            cmd.extend(['--python-version', python_version])

                        if self.implementation:
                            cmd.extend(['--implementation', self.implementation])
                        if self.abi:
                            cmd.extend(['--abi', self.abi])
                        if self.find_links:
                            for link in self.find_links:
                                cmd.extend(['-f', link])

                        if not self.trusted_hosts:
                            self.trusted_hosts = [urlparse(host).netloc for host in self.index_urls]
                        for host in self.trusted_hosts:
                            cmd.extend(['--trusted-host', host])


                        cmd.extend(['--only-binary=:all:', '--no-binary=:none:'])
                        if self.prefer_binary:
                            cmd.append('--prefer-binary')
                        if self.pre:
                            cmd.append('--pre')
                        if self.no_cache_dir:
                            cmd.append('--no-cache-dir')
                        if self.no_build_isolation:
                            cmd.append('--no-build-isolation')
                        if self.constraint_file:
                            cmd.extend(['-c', self.constraint_file])

                        # 执行命令
                        subprocess.run(cmd, check=True)

                        # # 移动下载的文件到正确的目录
                        # for filename in os.listdir(subdirectory):
                        #     src = os.path.join(subdirectory, filename)
                        #     dst = os.path.join(self.download_path, package_name, filename)
                        #     shutil.move(src, dst)
                        #
                        # # 删除空的子目录
                        # os.rmdir(subdirectory)

    def create_pypi_index(self):
        """
        创建依赖包的 PyPI 服务器索引。
        """
        cmd = ['dir2pi',self.download_path,'-S']
        subprocess.run(cmd, check=True)




