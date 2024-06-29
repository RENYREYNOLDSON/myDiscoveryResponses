###### APP TESTS
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2024
###### TESTS PDF FILES THROUGH THE CONVERTER PROGRAM

from converter import *
import os

LOCATION = r"C:\Users\reyno\Desktop\Freelancing\myDiscoveryResponses TESTS"

FILES = [["2024-05-21 WILLIS-ALBRIGO Def DFP",19,"RFP"],
         ["Def FRogs to Sean",59,"FROG"],
         ["Def SROGS to Sean (07944622xA9B4D)",37,"SPROG"],
         ["TM RPD(3) to Plaintiff 1-29-24",21,"RFP"]]


passed = 0
for f in FILES:
    filename = os.path.join(LOCATION,f[0])+".pdf"
    reqs,req_type,doc_details,custom_keys = getRequests(filename)
    if len(reqs)==f[1] and req_type==f[2]:#TEST PASSED
        print("✓ "+str(f[0]))
        passed+=1
    else:#TEST FAILED
        print("❌ FAILED: "+str(f)+"\n"+str(len(reqs))+"  "+str(req_type))

print("----------------------------\n")
print(str(passed)+"/"+str(len(FILES))+" Tests Passed!")