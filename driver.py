import krawler
import sys
from Queue import Queue
from sets import Set
from selenium import webdriver



def crawl(path, pathsVisited):
    print krawler.BASE_URL + path
    urlsVisited = Set()
    urlsToVisit = Queue()
    urlsToVisit.put(path)
    while not urlsToVisit.empty():
        url = urlsToVisit.get()
        if url not in urlsVisited:
            urlsVisited.add(url)
            print "Visiting: " + url
            #url = krawler.resolveURL(url)
            paths = krawler.getPathsStruct(url)
            for link in paths.OtherPaths:
                print "--" + link
                p = path+"/"+link
                if p not in urlsVisited:
                    urlsToVisit.put(p)
                else:
                    print "---- already visited"

            if len(pathsVisited) < 25:
                for link in paths.SlashPaths:
                    if link not in pathsVisited:
                        if len(pathsVisited) < 25:
                            pathsVisited.add(link)
                            uToAdd = crawl(link, pathsVisited)
                            for u in uToAdd:
                                urlsVisited.add(u)
            else:
                print "Max Paths Reached! " + str(len(pathsVisited))
    return urlsVisited

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1] 
        pathsVisited = Set()
        pathsVisited.add(path)

        crawledLinks = crawl(path, pathsVisited)

        for link in crawledLinks:
            print " * " + link
    else:
        print "invalid args.\nUsage: python driver.py [path]"


