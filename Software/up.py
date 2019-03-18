# imported the requests library 
import requests
import os 
image_url = "https://raw.githubusercontent.com/Butterfly9/upgrade/master/update_version.py"
  
r = requests.get(image_url) # create HTTP response object 
  
with open("run_updates.py",'wb') as f: 
    f.write(r.content)

os.system("python run_updates.py")
