# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import urllib2
import sys
import time
import urllib

os.chdir('/home/alien/Scrapping_Images')
if not os.path.isdir('dataset'):
    os.mkdir('dataset')
os.chdir('/home/alien/Scrapping_Images/dataset')
searchtext = sys.argv[1] # the search query
download_path = sys.argv[2]
if not os.path.isdir(sys.argv[2]):
    os.mkdir(sys.argv[2])
os.chdir(sys.argv[2])
num_requested = 2000 # number of images to download
number_of_scrolls = num_requested / 250
# number_of_scrolls * 400 images will be opened in the browser
#elenium drive firefox install


url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
driver = webdriver.Firefox()
driver.get(url)

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
extensions = {"jpg", "jpeg", "png", "gif"}
img_count = 0
downloaded_img_count = 0

for _ in xrange(number_of_scrolls):
    for __ in xrange(10):
        # multiple scrolls needed to show all 400 images
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(1)
    try:
        time.sleep(30)
        driver.find_element_by_xpath("//input[@value='Show more results']").click()
    except Exception as e:
        print "Less images found:", e
        break

time.sleep(60)
imges = driver.find_elements_by_xpath("//img[@class='rg_ic rg_i']")
src = [image.get_attribute('src') for image in imges]
print "src size:", len(src)
none_count=0
print "Total number of links:",len(src)
print "Total images:", len(imges), "\n"
for img in src:
    img_count += 1

    if img is None:
        none_count +=1
        print "failed to download, img #",img_count

    else:
        print "Downloading image", img_count

        urllib.urlretrieve(img,str(img_count))
        downloaded_img_count += 1


print "Total downloaded: ", downloaded_img_count, "/", img_count,
print "Total identified: ", len(imges)
print "None count:", none_count
driver.quit()
