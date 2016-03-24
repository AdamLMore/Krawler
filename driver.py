# Provides main driver code for the zite crawler.

import krawler
import sys
import thread
import threading
from Queue import Queue
from sets import Set
from selenium import webdriver


MAX_PATHS = 50 #Max new paths to branch to
ZITE_PATH_FILE = "Paths.dat"
ZITE_ALL_PATHS_FILE = "AllPaths.dat"
MAX_THREADS = 10
urlsVisited = Set()
pathsVisited = Set()

def crawl(path, pathsVisited, ziteAllPathsFile, zitePathFile):
    print krawler.BASE_URL + path
    urlsToVisit = Queue()
    urlsToVisit.put(path)
    while not urlsToVisit.empty():
        url = urlsToVisit.get()
        if url not in urlsVisited:
            urlsVisited.add(url)
            print "URLs Visited: " + str(len(urlsVisited))
            #print "Visiting: " + url
            paths = krawler.getPathsStruct(url)
            for link in paths.OtherPaths:
                #print "--" + link
                p = path+"/"+link
                if p not in urlsVisited:
                    ziteAllPathsFile.write(p.decode('UTF-8') + u"\n")
                    urlsToVisit.put(p)
                #else:
                    #print "---- already visited"

        if len(pathsVisited) < MAX_PATHS:
            if len(paths.SlashPaths) > 0:
                print "SlashPaths found: " + str(len(paths.SlashPaths))
            for link in paths.SlashPaths:
                if link not in pathsVisited:
                    print " > " + link
                    print "Paths Visited: " + str(len(pathsVisited)) + "/" + str(MAX_PATHS)
                    if len(pathsVisited) < MAX_PATHS:
                        zitePathFile.write(link.decode('UTF-8')+u"\n")
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


