# Provides main driver code for the zite crawler.

import krawler
import sys
import thread
import threading
from Queue import Queue
from sets import Set
from selenium import webdriver

reload(sys)
sys.setdefaultencoding("utf-8")

MAX_PATHS = 1000  #Max new paths to branch to
MAX_URLS  = 6000 #Max URLs to visit
ZITE_PATH_FILE = "Paths.dat"
ZITE_ALL_PATHS_FILE = "AllPaths.dat"
MAX_THREADS = 10
urlsVisited = Set()
pathsVisited = Set()
urlsInQueue = Set()

def crawl(path, pathsVisited, ziteAllPathsFile, zitePathFile):
    print krawler.BASE_URL + path
    urlsToVisit = Queue()
    urlsToVisit.put(path)
    while not urlsToVisit.empty() and len(urlsVisited) < MAX_URLS:
        url = urlsToVisit.get()

        if url.endswith("/"):
            url = url[:-1]

        if url not in urlsVisited:
            urlsVisited.add(url)
            ziteAllPathsFile.write(url.encode('UTF-8') + u"\n")
            print "URLs Visited: " + str(len(urlsVisited))
            #print "Visiting: " + url
            paths = krawler.getPathsStruct(url)
            print str(len(paths.HTTPPaths)) + " " + str(len(paths.OtherPaths)) + " " + str(len(paths.SlashPaths))
            for link in paths.OtherPaths:
                #print "--" + link
                p = path+"/"+link
                if p.endswith("/"):
                    p = p[:-1]
                if p not in urlsInQueue:
                    urlsInQueue.add(p)
                    urlsToVisit.put(p)
                    
                #else:
                    #print "---- already visited"

            if len(pathsVisited) < MAX_PATHS:
                if len(paths.SlashPaths) > 0:
                    print "SlashPaths found: " + str(len(paths.SlashPaths))
                for link in paths.SlashPaths:
                    if link.endswith("/"):
                        link = link[:-1]
                    if link not in pathsVisited:
                        print " > " + link
                        print "Paths Visited: " + str(len(pathsVisited)) + "/" + str(MAX_PATHS)
                        if len(pathsVisited) < MAX_PATHS:
                            zitePathFile.write(link.encode('UTF-8')+u"\n")
                            pathsVisited.add(link)
                            crawl(link, pathsVisited, ziteAllPathsFile, ziteAllPathsFile)
            else:
                print "Max Paths Reached! " + str(len(pathsVisited))
    return urlsVisited

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1] 
        pathsVisited = Set()
        pathsVisited.add(path)
        zitePathFile = open(ZITE_PATH_FILE, 'a')
        ziteAllPathsFile = open(ZITE_ALL_PATHS_FILE, 'a')
        crawledLinks = crawl(path, pathsVisited, ziteAllPathsFile, zitePathFile)

        for link in crawledLinks:
            print " * " + link
    else:
        print "invalid args.\nUsage: python driver.py [path]"


