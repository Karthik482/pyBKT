import numpy as np
def convert_data(df3):
  # find out how many problems per user, form the start/length arrays
  data=[x["correct"] for x in df3]
  starts, lengths=[],[]
  counter, lcounter = 1, 0
  prev_id = -1
  
  for i in df3:
      if i["user_id"] != prev_id:
          starts.append(counter)
          prev_id = i["user_id"]
          lengths.append(lcounter)
          lcounter = 0
      lcounter += 1
      counter += 1
  lengths.append(lcounter-1)
  lengths = np.asarray(lengths[1:])
      
  resource_ref = {}
  if "resource" in df3[0]:
    resources = []
    counter = 1
    for i in df3:
      if i["resource"] in resource_ref:
        resources.append(resource_ref[i["resource"]])
      else:
        resource_ref[i["resource"]] = counter
        counter += 1
        resources.append(resource_ref[i["resource"]])
  else:
    resources=[1]*len(data)
        
        
  Data={}
  gs_ref = {}
  if "gs" in df3[0]:
    num_gs = 0
    counter = 1
    for i in df3:
      if i["gs"] not in gs_ref:
        gs_ref[i["gs"]] = counter
        counter += 1
    data_temp = [[] for _ in range(len(gs_ref))]

    counter = 0
    for i in df3:
      for j in range(len(gs_ref)):
        if gs_ref[i["gs"]] == j:
            data_temp[j].append(data[counter])
            counter += 1
        else:
            data_temp[j].append(0)
    Data["data"]=np.asarray(data_temp,dtype='int32')
  else:
    data = [data]
    Data["data"]=np.asarray(data,dtype='int32')
    
  resource=np.asarray(resources)
  stateseqs=np.copy(resource)

  Data["stateseqs"]=np.asarray([stateseqs],dtype='int32')
  Data["starts"]=np.asarray(starts)
  Data["lengths"]=np.asarray(lengths)
  Data["resources"]=resource
  Data["resource_names"]=resource_ref
  Data["gs_names"]=gs_ref
  if "resource" not in df3[0]:
    resource_ref["Overall Rate"]=1  
  if "gs" not in df3[0]:
    gs_ref["Overall Rate"]=1  
  
  
 
  
  return (Data)

