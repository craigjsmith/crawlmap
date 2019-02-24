from bs4 import BeautifulSoup
import networkx as nx
import pickle
from urllib.request import urlopen
import time
import socket

g = nx.DiGraph() #graph object
l = [] #list of last visited nodes in crawl
savename = "ips.pkl"
maxDepth = 2

def isInList(item, array):
    for element in array:
        if item == element:
            return True
    return False

def getBaseAddress(url):
    url = url.strip().rstrip()
    url = removeMostOfAddress(url)
    url = url.replace("https://","")
    url = url.replace("http://","")
    if url[-1] == "/":
        url = url[:len(url)-1]
    if url[:4] == "www.":
        url = url[4:]
    return url
    
def removeMostOfAddress(url):
    count = 0
    for index in range(len(url)):
        if url[index] == "/":
            count = count + 1
        elif url[index] == "?":
            return url[:index + 1]
        if count == 3:
            return url[:index + 1]
    return url

def getLinksFromHtml(html):
    soup = BeautifulSoup(html,"html.parser")
    linkTags=soup.find_all("a")
    linkList = []
    for link in linkTags:
        linkLocation = link.get("href")
        if linkLocation == None:
            continue
        if linkLocation[:4] == "http":
            linkList.append(linkLocation)
    return linkList

def loadGraph():
    global g
    global l
    with open(savename,"rb") as input_:
        tup = pickle.load(input_)
    g = tup[0]
    l = tup[1]

def saveGraph():
    global g
    global l
    with open(savename,"wb") as output:
        pickle.dump((g,l), output)

def getHtml(link):
    try:
        response = urlopen(link)
        #response.getcode() gets http response code
        return (response.read(),response.getcode())
    except:
        return False

def crawlAndBuild(startUrl,depth):
    if depth >= maxDepth:
        return
    global g
    global l
    html = getHtml(startUrl)
    if html == False:
        return
    else:
        html = html[0]
    linkList = getLinksFromHtml(html)
    g.add_node(getBaseAddress(startUrl),size=1)
    counter = 1
    for link in linkList:
        fullLink = link
        link = getBaseAddress(link)
        counter = counter + 1
        g.add_node(link)
        g.add_edge(getBaseAddress(startUrl),link)
        crawlAndBuild(fullLink, depth + 1)

startingUrl = "https://reddit.com"
crawlAndBuild(startingUrl,0)
saveGraph()

ipfilename = "ips.txt"
loadGraph()
uniqueIps = []
totalList = []
for item in g.nodes():
    try:
        ipNum = socket.gethostbyname(item)
    except:
        continue
    try:
        index = uniqueIps.index(ipNum)
        totalList[index] = totalList[index] + 1
    except:
        uniqueIps.append(ipNum)
        totalList.append(1)
    ipFile = open(ipfilename,"w",encoding='utf-8')
    for index in range(len(uniqueIps)):
        ipFile.write(uniqueIps[index] + "," + str(totalList[index]) + "\n")
    ipFile.close()