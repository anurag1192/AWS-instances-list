import os,sys
import boto3
import json
def get_instances(tagkey):
    ec2client = boto3.client('ec2')
    instances_list = ec2client.describe_instances()
    #print instances_list["Reservations"]
    # temp list to store results with duplicates
    temp_list = []
    #reservation gets the instance details
    for reservation in instances_list["Reservations"]:
        for instance in reservation["Instances"]:
            #to store the details like instance id, tag value in dictionary
            res = {}
            #comparing instanceid and curr instance id to eliminate duplicate owners
            instanceid = ""
            #to get the value of all tags associated in Tags of instance
            for tag in instance["Tags"]:
                currinstanceid = instance["InstanceId"]
                ''' if key is owner then add the values to res dict and append to temp_list
                    We can change the logic here to multiple owner tags
                    We can get additional instance details using instace[""] and append to list of dicts
                    if the tagkey matches the given input'''
                if tag["Key"] == tagkey:
                    res['InstanceId'] = instance["InstanceId"]
                    res['Tag Value'] = tag["Value"]
                    res['InstanceType'] = instance["InstanceType"]
                    res['LaunchTime'] = str(instance["LaunchTime"])
                    temp_list.append(res)
                    instanceid = currinstanceid
                #else add values with unknown tag value to dict and append to temp_list
                elif instanceid != currinstanceid:
                    res['InstanceId'] = instance["InstanceId"]
                    res['Tag Value'] = "unknown"
                    res['InstanceType'] = instance["InstanceType"]
                    res['LaunchTime'] = str(instance["LaunchTime"])
                    temp_list.append(res)
                    instanceid = currinstanceid
    #final result list to remove duplicate instance id which has owner tag and unknown tags in instance details
    result = []
    for item in temp_list:
        if item not in result:
            result.append(item)
    # print result in json format for pretty output
    print "result = \n" , json.dumps(result, indent=4)

    # same logic as above to remove duplicates in one liner
    #result = [dict(item) for item in set([tuple(entry.items()) for entry in temp_list])]
    #print json.dumps(result, indent=4)

    # to access each instance in the result list
    #for item in result:
    #    print item or  item["InstanceId"] or item["Tag Value"]

#call the function using "python list_instances.py Owner" ---> Owner being the input
if __name__ == '__main__':
    tagkey = sys.argv[1]
    get_instances(tagkey)
