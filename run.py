import os

os.chdir('scraper')
exec(open("simple_scraper.py").read())
os.chdir('../ipgeo')
exec(open("ipgeo.py").read())
