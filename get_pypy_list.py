# 从配置的清华源获取requirements列表，如果不需要全部同步，可以不执行当前方法，自行选择

import requests
import re
report = requests.request('get','https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/')
text_str = str(report.text).split('\n')
with open('pypi_requirements.txt','w+') as f:
    for i in text_str:
        temp = re.findall('<a href="(.*?)/">',i)
        if temp != []:
            f.write(str(temp[0])+'\n')
 