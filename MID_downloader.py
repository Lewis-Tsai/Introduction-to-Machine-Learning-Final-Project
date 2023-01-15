import requests 
from bs4 import BeautifulSoup 
  
# specify the URL of the archive here 
archive_url = "https://midkar.com/jazz/jazz_01.html"
  
def get_midi_links(): 
      
    # create response object 
    r = requests.get(archive_url) 
      
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html5lib') 
      
    # find all links on web-page 
    links = soup.findAll('a') 
  
    # filter the link sending with .mp4 
    midi_links = [archive_url + link['href'] for link in links if link['href'].endswith('mid')] 
  
    return midi_links 
  
  
def download_midi_series(midi_links): 
  
    for link in midi_links: 
  
        '''iterate through all links in midi_links 
        and download them one by one'''
          
        # obtain filename by splitting url and getting 
        # last string 
        file_name = link.split('/')[-1] 
  
        print( "Downloading file:%s"%file_name) 
          
        # create response object 
        r = requests.get(link, stream = True) 
          
        # download started 
        # download the files to the assigned path
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)
          
        print( "%s downloaded!\n"%file_name )
  
    print ("All midi downloaded!")
    return
  
  
if __name__ == "__main__": 
  
    # getting all midi links 
    midi_links = get_midi_links() 
    # for i, s in enumerate(midi_links):
    #     midi_links[i] = midi_links[i].replace("jazz_01.html", "")
    # print(midi_links)
  
    # download all midi 
    download_midi_series(midi_links) 