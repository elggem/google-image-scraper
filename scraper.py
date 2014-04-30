#!/usr/bin/python2.7

from apiclient.discovery import build
import tempfile
import pycurl
import os


def get_filename_parts_from_url(url):
    fullname = url.split('/')[-1].split('#')[0].split('?')[0]
    t = list(os.path.splitext(fullname))
    if t[1]:
        t[1] = t[1][1:]
    return t

def retrieve(url, filename=None):
    if not filename:
        garbage, suffix = get_filename_parts_from_url(url)
        f = tempfile.NamedTemporaryFile(suffix = '.' + suffix, delete=False)
        filename = f.name
    else:
        f = open(filename, 'wb')
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(url))
    c.setopt(pycurl.WRITEFUNCTION, f.write)
    try:
        c.perform()
    except:
        filename = None
    finally:
        c.close()
        f.close()
    return filename

service = build("customsearch", "v1", developerKey="** YOUR DEVELOPER KEY**")

download_directory = 'images'
searchterm = 'butterfly'
number_of_results = 100 #should be divisible by 10, maximum imposed by google is 100
start_counter = 1

while start_counter < number_of_results:
    res = service.cse().list(
	      q=searchterm,
	      cx='** YOUR CX KEY**',
	      searchType='image',
	      start=start_counter,
	      num=10,
	      imgType='photo',
	      fileType='jpg',
	      safe= 'off'
    ).execute()

    if not 'items' in res:
	      print 'No result !!\nres is: {}'.format(res)
    else:
	      directory = download_directory+"/"+searchterm;
	      
	      if not os.path.exists(directory):
	        os.makedirs(directory)
	      
	      count = start_counter + 0
	      
	      for item in res['items']:
	          print(item['title'] + " at " + item['link'])
	          retrieve(item['link'], directory+"/"+"%010d" % count+".jpg")
	          count = count + 1
	          
    start_counter = start_counter + 10
