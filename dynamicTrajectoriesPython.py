import numpy as np
import matplotlib as plt
import math
import os
#Author:Sean Pagani
#python dynamic movement

#Creating character data sturctures
characters={"character_stop":
            {
            "id":161,
            "steering_behavior":1,
            "position": np.array([0,0]),
            "velocity":np.array([0,0]),
            "linear":np.array([0,0]),
            "angular":0,
            "orientation":0,
            "max_speed":0,
            "speed":0,
            "max_acceleration":0,
            "rotation": 0,
            },
  "character_seek":{
            "id":163,
            "steering_behavior":3,
            "position": np.array([50,-25]),
            "velocity":np.array([-4,-6]),
            "orientation":math.pi*3/2,
            "linear":np.array([0,0]),
            "target":1,
            "rotation": 0,
            "target_radius":0,
            "slow_radius":0,
            "time_to_target":0,
            "max_speed":8,
            "max_acceleration":2,
			      "avoid_radius":2
            },
    
    "character_flee":{
            "id":162,
            "steering_behavior":4,
            "position": np.array([-25,50]),
            "velocity":np.array([0,-8]),
            "orientation":math.pi/4,
            "max_speed":10,
            "max_acceleration":2,
            "linear":np.array([0,0]),
            "target":1,
            "rotation": 0,
            "target_radius":0,
            "slow_radius":0,
            "time_to_target":1,
			      "avoid_radius":2
            },
  "character_arrive":{
            "id":164,
            "steering_behavior":5,
            "position": np.array([-50,-75]),
            "velocity":np.array([-6,-4]),
            "orientation":math.pi,
            "max_speed":8,
            "max_acceleration":2,
            "linear":np.array([0,0]),
            "target":1,
            "rotation": 0,
            "target_radius":1,
            "slow_radius":26,
            "time_to_target":1,
			      "avoid_radius":2
            }
}
#separating arrive functions
arrive_debug={"character_stop":
            {
            "id":161,
            "steering_behavior":1,
            "position": np.array([0,0]),
            "velocity":np.array([0,0]),
            "linear":np.array([0,0]),
            "angular":0,
            "orientation":0,
            "max_speed":0,
            "speed":0,
            "max_acceleration":0,
            "rotation": 0,
            },
            "character_arrive":{
            "id":164,
            "steering_behavior":5,
            "position": np.array([-50,-75]),
            "velocity":np.array([-6,-4]),
            "orientation":math.pi,
            "max_speed":8,
            "max_acceleration":2,
            "linear":np.array([0,0]),
            "target":1,
            "rotation": 0,
            "target_radius":1,
            "slow_radius":26,
            "time_to_target":1,
			      "avoid_radius":2
            }

}
#Support functions
def vectorLength(vector):
  #Support function for getting length of vector
  return math.sqrt(vector[0]**2 + vector[1]**2)

def vectorNormalize(vector):
  #Support function for normalizing vector
  if vectorLength(vector) != 0:
    return np.array([vector[0] / vectorLength(vector), vector[1] / vectorLength(vector)])
  else:
    return np.array([0,0])




def seek(character,target):
    #create dict of steering and calculate seek path
    steering={"linear":np.array([0,0]),"angular": 0 }
    steering["linear"]=target["position"]-character["position"]#direction of target
    steering["linear"] = vectorNormalize(steering["linear"])#normalize linear
    steering["linear"]= steering["linear"]*character["max_acceleration"]
    steering["angular"]= 0
    return steering


def arrive(character,target):
    #create dict of steering and calculate arrival path
    steering={"linear":np.array([0,0]),"angular": 0 }
    direction=target["position"]-character["position"]#THE DIRECTION OF THE TARGET
    distance= vectorLength(direction)

    if distance < character["target_radius"]:
      target["speed"]= 0
    elif distance > character["slow_radius"]:
      target["speed"]= character["max_speed"]
    else:
      target["speed"]= character["max_speed"]*distance / character["slowradius"]
    
    target["velocity"]=vectorNormalize(direction)*target["speed"]
    steering["linear"] = target["velocity"]-character["velocity"]
    steering["linear"]= steering["linear"] / character["time_to_target"]

    if vectorLength(steering["linear"])>character["max_acceleration"]:
      steering["linear"] = vectorNormalize(steering["linear"])
      steering["linear"]= steering["linear"]*character["max_acceleration"]
    
    steering["angular"]=0

    return steering


def flee(character,target):
    #charcter flee function ported from R code
    steering={"linear":np.array([0,0]),"angular": 0 }
    steering["linear"]=character["position"]-target["position"] #THE DIRECTION OF THE TARGET
    steering["linear"] = vectorNormalize(steering["linear"])
    steering["linear"]= steering["linear"]*character["max_acceleration"]
    steering["angular"]= 0
    return steering

def stop(mover):
  #simple stop character ported from R code
  result={"linear":np.array([0,0]),"angular": 0 }
  result["linear"]= mover["velocity"]
  if vectorLength(result["linear"]) > mover["max_acceleration"]:
    result["linear"] = vectorNormalize(result["linear"])
    result["linear"] = result["linear"] * mover["max_acceleration"]
  result["angular"]  = -mover["rotation"]
  return result
    
def update(mover,steering,delta_time):
  #implement character movements
  mover["position"]=mover["position"] + (mover["velocity"]* delta_time)
  mover["orientation"]=mover["orientation"] + (mover["rotation"]*delta_time)
  mover["velocity"] = mover["velocity"] + (steering["linear"] * delta_time)
  mover["rotation"] = mover["rotation"] + (steering["angular"] * delta_time)
  
  if vectorLength(mover["velocity"]) > mover["max_speed"]:#check if velocity is greater than max spped
    mover["velocity"]= vectorNormalize(mover["velocity"])
    mover["velocity"]= mover["velocity"] * mover["max_speed"]
  if vectorLength(mover["velocity"])< stop_speed:
    mover["velocity"] = np.array([0,0])
  if mover["rotation"] < stop_rotate:                
    mover["rotation"] = 0       
  return mover

Time=-.5 #starting time
stop_speed=0.01#avoid jitter
stop_rotate=0.01
delta_time=0.5
stop_time=50

while Time < stop_time:
  #game while loop 0+0.5..50.0
  Time=Time+delta_time
  for character in characters:
    if characters[character]["steering_behavior"]== 1:
      steering=stop(characters["character_stop"])
    
    if characters[character]["steering_behavior"]== 3:
      steering=seek(characters["character_seek"],characters["character_stop"])
      
    if characters[character]["steering_behavior"]== 4:
      steering=flee(characters["character_flee"],characters["character_stop"])

    if characters[character]["steering_behavior"]== 5:
      steering=arrive(arrive_debug["character_arrive"],arrive_debug["character_stop"])
    #updating linear directions
    characters[character]["linear"]= steering["linear"]
    characters[character]["angular"]= steering["angular"]
    #apply steering using update function
    characters[character]=update(characters[character],steering,delta_time)
    #printing output to console and to text file
    print(Time,
    characters[character]["id"],
    characters[character]["position"][0],
    characters[character]["position"][1],
    characters[character]["velocity"][0],
    characters[character]["velocity"][1],
    characters[character]["linear"][0],
    characters[character]["linear"][1],
    characters[character]["orientation"],
    characters[character]["steering_behavior"])
    
    output=Time,\
    characters[character]["id"],\
    characters[character]["position"][0],\
    characters[character]["position"][1],\
    characters[character]["velocity"][0],\
    characters[character]["velocity"][1],\
    characters[character]["linear"][0],\
    characters[character]["linear"][1],\
    characters[character]["orientation"],\
    characters[character]["steering_behavior"]
    with open ("Trajecory.txt","a") as file:
      file.writelines(','.join(map(str,output))+'\n')
#end program
