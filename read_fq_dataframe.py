from datetime import datetime
import pandas as pd
import json
import pickle

with open('fq_dataframe.pickle', 'rb') as f:
    fq = pickle.load(f)
