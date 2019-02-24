import json
from urllib.request import urlopen

output = open("locations.txt", "w")

ips = '../scraper/ips.txt'  
with open(ips) as fp:  
   line = fp.readline()
   while line:
        try:
            print(line)
            apicall = "http://api.ipstack.com/" + line.split(",")[0].rstrip() + "?access_key=a8b8d0606d4a392c76c248be3dafc552"
            print(apicall)
            response = urlopen(apicall).read()
        except:
            pass

        data = json.loads(response)
        lat = data["latitude"]
        lon = data["longitude"]
      
        occur = int(line.split(",")[1])
        for i in range(occur):
            output.write(str(lat) + "," + str(lon) + "\n")

        line = fp.readline()

output.close()