import numpy as np
import cv2
import imutils
import pytesseract
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

strInput = pytesseract.image_to_string(image)
print(strInput)

# type(strInput) = str
# string to json
import random
import string

def randomString(stringLength):
# Generate a random string 
# with the combination of lowercase and uppercase letters
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

# determine if this string is the first blocks
# (need to set "topLevel":true ,and "x","y")
index = 0 

# this array is to record all the block's name
blockName = []

# this dict is to construct the content of "blocks"
d = {}

#NumBrick = 7
i = 1
lines = strInput.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    print('line: ', line)
    print('i= ', i)
    i = i+1
    # get the most similar string (use FuzzyWuzzy package)
    strOptions = ["when flag clicked", "move steps", "turn clockwise degrees"
                  , "turn counterclockwise degrees", "wait seconds", "say hello!"
                  , "go to x : y :"]
    AllRatios = process.extract(line, strOptions)
    print(AllRatios)
    HighestRatios = process.extractOne(line, strOptions)
    print(HighestRatios)
    print(HighestRatios[0])
    print(HighestRatios[1])

    # get block's (random) name
    # and then record into array
    strName = randomString(10)
    blockName.append(strName)

    d[blockName[index]] = {}


    if index == 0:
        d[blockName[index]]['parent'] = None
        d[blockName[index]]['topLevel'] = True
        d[blockName[index]]['x'] = 86
        d[blockName[index]]['y'] = 142
    else:
        d[blockName[index]]['parent'] = blockName[index-1]
        d[blockName[index]]['topLevel'] = False

    if index > 0:
        d[blockName[index-1]]['next'] = blockName[index]

    # add content inside "blocks" corresponding to "identified toy bricks"
    # (with the same DICT to "isStage": false,)
    if HighestRatios[0] == "when flag clicked": #done
        d[blockName[index]]['opcode'] = 'event_whenflagclicked'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    elif HighestRatios[0] == "move steps": #done
        d[blockName[index]]['opcode'] = 'motion_movesteps'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['inputs']['STEPS']= []
        d[blockName[index]]['inputs']['STEPS'].append(1)
        d[blockName[index]]['inputs']['STEPS'].append([4,'10']) # '10' means move 10 steps
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    elif HighestRatios[0] == "turn clockwise degrees": #done
        d[blockName[index]]['opcode'] = 'motion_turnright'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['inputs']['DEGREES']= []
        d[blockName[index]]['inputs']['DEGREES'].append(1)
        d[blockName[index]]['inputs']['DEGREES'].append([4,'15']) # '15' means turn 15 degrees
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    elif HighestRatios[0] == "turn counterclockwise degrees": #done 
        d[blockName[index]]['opcode'] = 'motion_turnleft'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['inputs']['DEGREES']= []
        d[blockName[index]]['inputs']['DEGREES'].append(1)
        d[blockName[index]]['inputs']['DEGREES'].append([4,'15']) # '15' means turn 15 degrees
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    elif HighestRatios[0] == "wait seconds": #done
        d[blockName[index]]['opcode'] = 'control_wait'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['inputs']['DURATION']= []
        d[blockName[index]]['inputs']['DURATION'].append(1)
        d[blockName[index]]['inputs']['DURATION'].append([5,'1']) # '1' means "wait 1 second"
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    elif HighestRatios[0] == "say hello!":  #done
        d[blockName[index]]['opcode'] = 'looks_say'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['inputs']['MESSAGE']= []
        d[blockName[index]]['inputs']['MESSAGE'].append(1)
        d[blockName[index]]['inputs']['MESSAGE'].append([10,'Hello!']) # 'Hello!' means "say Hello!"
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    elif HighestRatios[0] == "go to x : y :":#done
        d[blockName[index]]['opcode'] = 'motion_gotoxy'
        d[blockName[index]]['inputs']= {}
        d[blockName[index]]['inputs']['X']= []
        d[blockName[index]]['inputs']['X'].append(1)
        d[blockName[index]]['inputs']['X'].append([4,'0']) # '0' means "set x to 0"
        d[blockName[index]]['inputs']['Y']= []
        d[blockName[index]]['inputs']['Y'].append(1)
        d[blockName[index]]['inputs']['Y'].append([4,'0']) # '0' means "set y to 0"
        d[blockName[index]]['fields'] = {}
        d[blockName[index]]['shadow'] = False

    index = index+1


#else:

d[blockName[index-1]]['next'] = None
#print("###############################")
#print("### all the block content : ###")
#print("###############################")
#print(d)
#print("###############################")
#print("#### all the block JSON : #####")
#print("###############################")
#print(json.dumps(d))




    #read JSON from a file
    # (JSON file with NO CONTENT IN "blocks")
'''
	with open('edit_NO_BLOCK_CONTENT.json') as json_file:
		data = json.load(json_file)

############## THIS PART WASN'T FINISHED YET #############
# when all toy bricks is done, stick "d" to "blocks"
# (with the same DICT to "isStage": false,)
	if "targets" in data

	# write JSON to a file
	with open('project.json', 'w') as outfile:
		json.dump(data, outfile)
'''
#######################################################################
# problem :
# 1. need to identify number
# 	e.g. "move 10 steps"
# 	=> "10" need to be identify  and assign to corresponding dict value
# 	this program just set to fixed number
# 	(<- this part need to change, and then set to a variable)

tmp_targets_dic_to_obj = [
    {
    "isStage": True,
    "name": "Stage",
    "variables": {
        "`jEk@4|i[#Fk?(8x)AV.-my variable": [
        "my variable",
        0
        ]
    },
    "lists": {},
    "broadcasts": {},
    "blocks": {},
    "comments": {},
    "currentCostume": 0,
    "costumes": [
        {
        "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
        "name": "backdrop1",
        "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
        "dataFormat": "svg",
        "rotationCenterX": 240,
        "rotationCenterY": 180
        }
    ],
    "sounds": [
        {
        "assetId": "83a9787d4cb6f3b7632b4ddfebf74367",
        "name": "pop",
        "dataFormat": "wav",
        "format": "",
        "rate": 44100,
        "sampleCount": 1032,
        "md5ext": "83a9787d4cb6f3b7632b4ddfebf74367.wav"
        }
    ],
    "volume": 100,
    "layerOrder": 0,
    "tempo": 60,
    "videoTransparency": 50,
    "videoState": "on",
    "textToSpeechLanguage": None
    },
    {
    "isStage": False,
    "name": "Sprite1",
    "variables": {},
    "lists": {},
    "broadcasts": {},
    "blocks": {
        ######################################
		
        "1": {
        "opcode": "event_whenflagclicked",
        "next": "[+6|s2ee%5ZMFcdzIj1M",
        "parent": None,
        "inputs": {},
        "fields": {},
        "shadow": False,
        "topLevel": True,
        "x": 285,
        "y": 332
        },
        "[+6|s2ee%5ZMFcdzIj1M": {
        "opcode": "motion_movesteps",
        "next": None,
        "parent": "1",
        "inputs": {
            "STEPS": [
            1,
            [
                4,
                "10"
            ]
            ]
        },
        "fields": {},
        "shadow": False,
        "topLevel": False
        }
		
        ######################################
    },
    "comments": {},
    "currentCostume": 0,
    "costumes": [
        {
        "assetId": "b7853f557e4426412e64bb3da6531a99",
        "name": "costume1",
        "bitmapResolution": 1,
        "md5ext": "b7853f557e4426412e64bb3da6531a99.svg",
        "dataFormat": "svg",
        "rotationCenterX": 48,
        "rotationCenterY": 50
        },
        {
        "assetId": "e6ddc55a6ddd9cc9d84fe0b4c21e016f",
        "name": "costume2",
        "bitmapResolution": 1,
        "md5ext": "e6ddc55a6ddd9cc9d84fe0b4c21e016f.svg",
        "dataFormat": "svg",
        "rotationCenterX": 46,
        "rotationCenterY": 53
        }
    ],
    "sounds": [
        {
        "assetId": "83c36d806dc92327b9e7049a565c6bff",
        "name": "Meow",
        "dataFormat": "wav",
        "format": "",
        "rate": 44100,
        "sampleCount": 37376,
        "md5ext": "83c36d806dc92327b9e7049a565c6bff.wav"
        }
    ],
    "volume": 100,
    "layerOrder": 1,
    "visible": True,
    "x": 130.18516525781368,
    "y": -30.763809020504144,
    "size": 100,
    "direction": 105,
    "draggable": False,
    "rotationStyle": "all around"
    }
]
tmp_meta_dic_to_obj = {
	"semver": "3.0.0",
	"vm": "0.2.0-prerelease.20190918022946",
	"agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
}

#template = {tmp_targets_dic_to_obj, tmp_monitors_dic_to_obj, tmp_extensions_dic_to_obj, tmp_meta_dic_to_obj}

tmp_targets_dic_to_obj[1]["blocks"] = d

template = {
    "targets": tmp_targets_dic_to_obj,
    "monitors": [],
    "extensions": [],
    "meta": tmp_meta_dic_to_obj
}

#print(tmp_targets_dic_to_obj[1]["blocks"])

with open('data.json', 'w') as f:
    json.dump(template, f)


