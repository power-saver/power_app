## Getting start

#### Prerequisites
* python 3.8.*
* mongodb 6.0.*
```
git clone https://github.com/power-saver/power_app.git
```

#### Create python virtaul environment
``` 
cd power_app
python -m venv power_venv
```
#### Activate Python virtual environment
```
source power_venv/bin/active
```

#### Install dependency packages
```
pip install -r requirements.txt
```

#### Load dataset (execute only once initially)
you need Api Key (https://bigdata.kepco.co.kr/cmsmain.do?scode=S01&pcode=000493&pstate=L&redirect=Y)
```
python load.py
```

#### Start App
```
uvicorn app.main:app --port 8080
```