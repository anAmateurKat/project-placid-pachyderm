#!/bin/bash

#This script tests the GET and POST endpoints using curl

url=http://127.0.0.1:5000/api/timeline_post
arr_len=$(curl $url | jq '.timeline_posts | length')

#create a timeline post
curl -X POST $url -d 'name=Placid&email=cidakat@outlook.com&content=Testing endpoints w/random timeline post'

#check if a timeline post was added
if [ $(curl -X GET $url | jq '.timeline_posts | length') -eq $((arr_len+1)) ]
then
	echo "Test - timeline post added: Success!"
fi

#delete the test timeline post
curl -X DELETE $url

