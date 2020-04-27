import sys
sys.path.append('../')
from pyBKT.util import model_helper
import os

def assistments_data(url, skill_name, resource_name=None, gs_name=None, multilearns2=False, multipriors=True):
  
  import pandas as pd
  import numpy as np
  import io
  import requests
  print(skill_name)
  df = None
  if url[:4] == "http":
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('latin')))
  else:
    f = open("data/" + url, "rb")
    
    df = pd.read_csv(io.StringIO(f.read().decode('latin')))
  # filter by the skill you want, make sure the question is an 'original'
  # skills = df["skill_name"]
  # for skill_name in skills:
  skill = df[(df["skill_name"]==skill_name) & (df["original"] == 1)]
  # sort by the order in which the problems were answered
  df["order_id"] = [int(i) for i in df["order_id"]]
  df.sort_values("order_id", inplace=True)
  
  # example of how to get the unique users
  # uilist=skill['user_id'].unique()

  # convert from 0=incorrect,1=correct to 1=incorrect,2=correct
  skill.loc[:,"correct"]+=1
  
  # filter out garbage
  df3=skill[skill["correct"]!=3]
  
  #store df3 as list of tuples (correct, user_id, problem_id, resource_name, gs_name)
  converted_df3 = []
  for i, j in df3.iterrows():
      temp = {}
      temp["correct"] = j["correct"]
      temp["user_id"] = j["user_id"]
      if resource_name is not None:
          temp["resource"] = j[resource_name]
      if gs_name is not None:
          temp["gs"] = j[gs_name]
      if multilearns2:
          temp["problem_id"] = j["problem_id"]
      converted_df3.append(temp)
  
  return model_helper.convert_data(converted_df3, multipriors)
  
  
 

