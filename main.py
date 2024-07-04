from SyncPypi import SyncPypi


if __name__ == "__main__":
    config = SyncPypi('config.json')
    config.execute_pip_download()
    config.create_pypi_index()
