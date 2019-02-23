from bs4 import BeautifulSoup
import networkx as nx
import pickle
import matplotlib
import matplotlib.pyplot as plt
from urllib.request import urlopen
import time
import socket
import os

g = nx.DiGraph() #graph object
l = [] #list of last visited nodes in crawl
savename = ""
maxDepth = 0
ipfile = open("iplist.txt","w",encoding = "utf-8")


def saveIp(link):
    try:
        ipfile.write(socket.gethostbyname(link) + "\n")
    except:
        pass

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
    g.add_node(startUrl)
    counter = 1
    for link in linkList:
        fullLink = link
        link = getBaseAddress(link)
##        print(fullLink)
##        print(link)
        print("\t" * depth + "Starting " + str(counter) + " out of " + str(len(linkList)))
        counter = counter + 1
        g.add_node(link)
        g.add_edge(getBaseAddress(startUrl),link)
        saveIp(link)
        crawlAndBuild(fullLink, depth + 1)
    if depth == 0:
        print("Finished Crawling")

while True:
    action = input("Command (help for options): ")
    clear = True
    if action == "gather":
        maxDepth = int(input("Max Depth of Tree: "))
        savename = input("Name to save map file: ") + ".pkl"
        startingUrl = input("URL to start search: ")
        #https://www.hackerone.com/blog/hacker-blogs-we-love-reading
        crawlAndBuild(startingUrl,0)
        saveGraph()
        ipfile.close()
    elif action == "plot":
        ipfile.close()
        savename = input("name of pickle file to plot: ") + ".pkl"
        loadGraph()
        nx.draw(g,with_labels=True)
        plt.show()
    elif action == "ipsFromPickle":
        pass
    elif action == "exit":
        exit()
    elif action == "help":
        clear = False
        print("gather")
        print("plot")
        print("ipsFromPickle")
        print("exit")
    else:
        print("Not a valid command")
        clear = False
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')

##g.add_node("name")
##g.add_edge("firstNode","ToSecondNode")
#nx.draw_circular(g)
#nx.draw_spectral(g)
