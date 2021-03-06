# Distributed AI

This repository contains two implementations of a semantic similarity application:
the first one using a pure, centralized, client-server architecture, while the
second uses a distributed blockchain.

Both implementations were tested on Google Chrome, Opera and Microsoft Edge browsers.

## Client-Server Architecture

### To turn the server on:

1. Create environment
```
python3 -m venv env
```

2. Activate environment
```
source env/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Start the server
```
cd server
flask run
```

Note that it is necessary to wait until the server is ready to open the client. A pre-trained machine learning model will be downloaded before the client is ready.

The message `Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)` shows the server is ready.


### To start the client:

Open the HTML file inside the `client/` folder using a browser.


### How to use

After opening the HTML file, type two sentences and click on the SEND button to verify how semantic similar the sentences are.

## Distributed Blockchain

. Create environment
```
conda env create -f environment.yml
```

2. Activate environment
```
conda activate distributed
```

3. Start the distributed blockchain application

`[--load_db]` is an optional command-line argument. If it's specified on execution,
then the blockchain will be initialized from an existing SQL database. Otherwise,
the blockchain will be created from scratch using a genesis block.

```
cd blockchain
python app.y [--load_db]
```

4. After starting the distributed blockchain application, open the interface on 

```
http://127.0.0.1:5000/
```