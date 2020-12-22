import os
import re

urlPattern = re.compile('<a href="(.+?)"')
urls=set()

with open('lego_urls.txt') as f:
    for line in f.readlines():
        match = urlPattern.findall(line)
        
        #if 'http' in line:
         #   print(line)
        
        if match:
            #print(match)
            urls.add(match[0])


with open('lego_urls.out.txt', 'w') as f:
    for url in urls:
        print(url)
        f.write(url)
