import json,sys
obj=json.load(sys.stdin)
score = obj["score"]
if score > int(5):
    print "SPAM"
