import json
from urllib.request import urlopen

output = open("locations.txt", "w")
first = True

ips = 'ips.txt'  
with open(ips) as fp:  
   line = fp.readline()
   while line:
        try:
            print(line)
            apicall = "http://api.ipstack.com/" + line.rstrip() + "?access_key=a8b8d0606d4a392c76c248be3dafc552"
            print(apicall)
            response = urlopen(apicall).read()
        except:
            pass

        data = json.loads(response)
        lat = data["latitude"]
        lon = data["longitude"]

        if(not first):
            output.write("\n")

        first = False        
        output.write(str(lat) + "," + str(lon))

        line = fp.readline()

output.close()