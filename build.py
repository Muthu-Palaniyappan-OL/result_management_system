import requests
import os
import struct
from zipfile import ZipFile
import shutil

def download_package(url :str):
    print('Downloading... ' + url)
    open('./build/python/pkg.whl', 'wb').write(requests.get(url, allow_redirects=True).content)

    print('Extracting... ' + url)
    with ZipFile('./build/python/pkg.whl') as zipfile:
        zipfile.extractall(path='./build/python/Lib')

    print('Finished ' + url)
    os.remove('./build/python/pkg.whl')

if __name__ == '__main__':

    if os.name != 'nt' or struct.calcsize("P") != 8:
        print('This build script works only for windows x64!')
        exit(1)
    
    os.makedirs('./build/python/Lib', exist_ok=True)

    if not os.path.exists('./build/python/python.exe'):
        print('Python doesnt exist in build.')
        print('Downloading python...')

        open('./build/python.zip', 'wb').write(requests.get('https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip', allow_redirects=True).content)
        with ZipFile('./build/python.zip') as zipfile:
            zipfile.extractall(path='./build/python')
        os.remove('./build/python.zip')

        download_package('https://files.pythonhosted.org/packages/36/42/015c23096649b908c809c69388a805a571a3bea44362fe87e33fc3afa01f/flask-3.0.0-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/c3/fc/254c3e9b5feb89ff5b9076a23218dafbc99c96ac5941e900b71206e6313b/werkzeug-3.0.1-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/bc/c3/f068337a370801f372f2f8f6bad74a5c140f6fda3d9de154052708dd3c65/Jinja2-3.1.2-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/44/44/dbaf65876e258facd65f586dde158387ab89963e7f2235551afc9c2e24c2/MarkupSafe-2.1.3-cp312-cp312-win_amd64.whl')
        download_package('https://files.pythonhosted.org/packages/68/5f/447e04e828f47465eeab35b5d408b7ebaaaee207f48b7136c5a7267a30ae/itsdangerous-2.1.2-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/00/2e/d53fa4befbf2cfa713304affc7ca780ce4fc1fd8710527771b58311a3229/click-8.1.7-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/fa/2a/7f3714cbc6356a0efec525ce7a0613d581072ed6eb53eb7b9754f33db807/blinker-1.7.0-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/d5/77/b34088cbb55ba59e1cc6512ab2ff3b7679102b7f7577982a96cbdcddb90c/tabula_py-2.9.0-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/ad/11/52fbe97fd84c91105b651d25a122f8deed6d3519afb14f9771fac1c9b7de/numpy-1.26.3-cp312-cp312-win_amd64.whl')
        download_package('https://files.pythonhosted.org/packages/ae/d9/3741b344f57484b423cd22194025a8489992ad9962196a62721ef9980045/pandas-2.1.4-cp312-cp312-win_amd64.whl')
        download_package('https://files.pythonhosted.org/packages/32/4d/aaf7eff5deb402fd9a24a1449a8119f00d74ae9c2efa79f8ef9994261fc2/pytz-2023.3.post1-py2.py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/36/7a/87837f39d0296e723bb9b62bbb257d0355c7f6128853c78955f57342a56d/python_dateutil-2.8.2-py2.py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/1d/6a/89963a5c6ecf166e8be29e0d1bf6806051ee8fe6c82e232842e3aeac9204/flask_sqlalchemy-3.1.1-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/53/80/3d94d5999b4179d91bcc93745d1b0815b073d61be79dd546b840d17adb18/greenlet-3.0.3-cp312-cp312-win_amd64.whl')
        download_package('https://files.pythonhosted.org/packages/1b/9e/3f86cf00c2245afb236205ab0fbdf7b77ac4ee931603e18b7e192315a514/SQLAlchemy-2.0.25-py3-none-any.whl')
        download_package('https://files.pythonhosted.org/packages/b7/f4/6a90020cd2d93349b442bfcb657d0dc91eee65491600b2cb1d388bc98e6b/typing_extensions-4.9.0-py3-none-any.whl')
        
        with open('./build/python/python312._pth', 'a') as f:
            f.write('Lib/\n')

    else:
        print('Not Downloading Packages... / Python.. Skipping')
    
    files = ['main.py', 'app.bat']
    folders = ['templates']
    for f in files:
        shutil.copy(f, "./build/" + f)
    for f in folders:
        shutil.rmtree("./build/" + f, ignore_errors=True)
    for f in folders:
        shutil.copytree(f, "./build/" + f)
    