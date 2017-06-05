# Commands (DEV)


### querying from audio

export FILE=f1.mp3

echoprint-codegen $FILE | jq -r > f1.data

curl -X POST \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d `cat f1.data` \
     "http://127.0.0.1:7777/api/v1/fprint/identify/"
