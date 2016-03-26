"""
Utility methods used in the Krawler.
Please Note: In order for this to work, all libraries must be installed,
and you must have PhantomJS Installer, and the path configured below.
All libraries can be installed using pip
"""

from bs4 import BeautifulSoup
import urllib2
import string
import Queue
import os
import time
from selenium import webdriver

BASE_URL = "http://127.0.0.1:43110"
PHANTOMJS_PATH = "/home/adam/phantomjs/bin/phantomjs"
browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_log_path=os.path.devnull)
browser.set_window_size(1400, 1000)

class PathsStruct:
    HTTPPaths = Queue.Queue()
    SlashPaths = Queue.Queue()
    OtherPaths = Queue.Queue()
    def __init__(self, HTTPPaths, SlashPaths, OtherPaths):
        self.HTTPPaths = HTTPPaths
        self.SlashPaths = SlashPaths
        self.OtherPaths = OtherPaths

def phantomResolve(url):
    #url = resolveURL(url)
    browser.get(BASE_URL + url)
    content = browser.page_source
    try:
        browser.switch_to.frame(browser.find_element_by_id("inner-iframe"))
    except:
        return content
    time.sleep(0.4) 
    content = browser.page_source
    return content 

def resolveURL(path):
    url = "http://127.0.0.1:43110" + path #12WY4MGfJDjuBjj692q9x4TH8S5fsfaMtm"
    #print "\nSource URL: " + url
    baseURL = "http://127.0.0.1:43110"


    try: 
        openURL = urllib2.urlopen(url)
    except:
        return baseURL+path

    content = openURL.read()
    soup = BeautifulSoup(content, "lxml")

    #print soup.prettify()
    s = ""
    i = 0
    script = soup.find_all('script')
    if len(script) > 1:
        if len(script[1]) > 0:
            s = script[1].contents[0]
        else:
            return baseURL+path
    else:
        return baseURL+path
    
    path = ""
    for l in s.splitlines():
        if l.startswith('document.getElementById("inner-iframe").src ='):
            path = l[47:-1].replace("\\", "")
    #print "Actual URL: " + baseURL + path
    return baseURL + path

def getLinks(url):
    returnQueue = Queue.Queue()
    try:
#        content = urllib2.urlopen(url).read()
        content = phantomResolve(url)
    except urllib2.HTTPError:
        return returnQueue
    soup = BeautifulSoup(content, "lxml")

    links = soup.find_all('a')
    next = ""
    for atag in links:
        if atag.has_attr('href'):
            returnQueue.put(atag['href'])
    return returnQueue

def getPathsStruct(url):
    linkQueue =  getLinks(url)
    queueList = []
    httpLinks = []
    slashLinks = []
    otherLinks = []
    link = ""
    while not linkQueue.empty():
        link = linkQueue.get()
        if link.startswith("http"):
            httpLinks.append(link)
        elif link.startswith("/"):
            slashLinks.append(link)
        else:
            otherLinks.append(link)
    queueList.append(httpLinks)
    queueList.append(slashLinks)
    queueList.append(otherLinks)
    return PathsStruct(httpLinks, slashLinks, otherLinks)
