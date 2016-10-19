# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 22:02:39 2016

@author: karan
"""
import json
import pandas as pd

allProblems = {}
userIdToNameAndLink = {"0" : ("NA", "http://placeholder")}
userNameToUserId = {"NA" : "0"}
tagIdToTagAndLink = {"0" : "NoTag"}
tagNameToTagId = {"NoTag" : "0"}
if __name__ == "__main__":
    problems = json.loads(open("json/problems.json").read())
    for problem in problems:
        Id = problem.keys()[0]
        allProblems[Id] = problem[Id]
    
    ## Loop to create a dict of users and then update userId in each problem
    userCounter = 0
    tagCounter = 0
    for problem in allProblems.values():
        if "added_by" in problem.keys():
            for name,link in problem["added_by"].iteritems():
                if name in userNameToUserId.keys():
                    problem["added_by"] = name
                else:                
                    userCounter += 1
                    userIdToNameAndLink[str(userCounter)] = (name,link)
                    userNameToUserId[name] = str(userCounter) 
                    problem["added_by"] = name
        else:
            problem["added_by"] = "NA"
        listOfTags = []
        for tag, tagLink in problem["tags"].iteritems():
            if tag in tagNameToTagId.keys():
                listOfTags.append(tagNameToTagId[tag])
            else:
                tagCounter += 1
                tagIdToTagAndLink[str(tagCounter)] = (tag, tagLink)
                tagNameToTagId[tag] = str(tagCounter)
                listOfTags.append(str(tagCounter))
        if len(listOfTags) == 0:
            listOfTags.append("0")
        problem["tags"] = ','.join(listOfTags)
    
    dfProblems = pd.DataFrame.from_dict(allProblems, orient='index')
    dfProblems.to_csv("json/problems.csv",index=False)
    dfUsers = pd.DataFrame.from_dict(userIdToNameAndLink, orient='index')
    dfUsers.to_csv("json/users.csv",index_label="UserId")
    dfTags = pd.DataFrame.from_dict(tagIdToTagAndLink, orient='index')
    dfTags.to_csv("json/tags.csv",index_label="TagId")