#!/bin/bash

pip install -r requirements.txt
python ./app/preprocess/makeindex.py
python ./app/preprocess/init_db.py