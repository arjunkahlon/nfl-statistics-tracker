# NFL-Stats

**1. Commands to run to prepare for your server**
  - Start bash
```
bash
```
  - Install virtual environment
```
python3 -m venv venv
```
  - Start your virtual environment
```
source venv/bin/activate
```
  - Install required modules
```
pip3 install flask
pip3 install requests
pip3 install flask flask-wtf
pip3 install flask_table
```
  - Create a config.py file by using bash shell to echo the contents of the file into config.py. {your port number} could be any port, 12122 for example. And {api key} is your api key
```
echo -e "PORT = {your port number}\nAPI_KEY = '{api key}'" >> config.py
```
  - For the above step, for example, if your port number were 12122 and your api key were oijweiotjowetoj, you would type:
```
echo -e "PORT = 12122\nAPI_KEY = 'oijweiotjowetoj'" >> config.py
```
**2. Run the python program**
  - Start your virtual environment
```
source venv/bin/activate
```
  - Run main program in python3
```
python3 nflstats.py
```
  - Run worker. Worker is a background task that makes API calls to send to server. Main program should be ran first and then the worker.
```
python3 worker.py
```
**3. To run forever**
  - Start your virtual environment
```
source venv/bin/activate
```
  - Run main program in python3
```
nohup python3 nflstats.py &
```
  - Run worker
```
nohup python3 worker.py &
```
**4. To stop your server after running forever**
  - Find your process ID(s) (find the command that ends with ".../flask/nflstats.py" and the command with "python3 worker.py"
```
ps aux | grep {your user name}
```
  - Then terminate your process ID(s)
```
kill -9 {processId}
```
**5. To open the website**
  - Log into OSU VPN
  - Open a web browser and enter flipX.engr.oregonstate.edu:{port}, where X in flipX is the same flip server that you are running your instance on. flip3 is one for example. {port} is the {port} that you set in config.py. For example, to reach one instance of the server, you could enter http://flip3.engr.oregonstate.edu:12121/ in your web browser address.
