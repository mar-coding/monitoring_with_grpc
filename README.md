# monitoring_with_grpc
monitor the server with the help of python3 and grpc protocol

## run(both in client and server)
```
git clone https://github.com/mar-coding/monitoring_with_grpc.git
cd monitoring_with_grpc
python3 -m venv venv
source venv/bin/activate
sudo chmod +x ./setup.sh
pip install -r req.txt
./setup.sh
```

### for server
```
python server.py
```

### for monitoring
```
python monitor.py
```

### for telegram

1. create a telegram bot in '@botfather' and get your bot's token.

2. create '.env' file and write this to it.(must be done in root directory):
```
TOKEN=bottoken
```

# To Do
- [ ] Solve the timing problem to logging become realtime
