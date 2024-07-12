###### APP TESTS
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2024
###### TESTS PDF FILES THROUGH THE CONVERTER PROGRAM

from converter import *
import os

LOCATION = r"C:\Users\reyno\Desktop\Freelancing\myDiscoveryResponses TESTS"

FILES = [["Def SROGS to Sean (07944622xA9B4D)",37,"SPROG"],
         ["TM RPD(3) to Plaintiff 1-29-24",21,"RFP"],
         ["2022-03-30 KLOTZLE Def RFA",1,"RFA"],
         ["2022-03-30 KLOTZLE Def RFP",15,"RFP"],
         ["2022-03-30 KLOTZLE Def Special Interrogatories",29,"SPROG"],
         ["2022-05-24 OWEN Def RFP1 [Quiroz] to Plf",14,"RFP"],
         ["2022-05-24 OWEN Def SRogs1 [Quiroz] to Plf",18,"SPROG"],
         ["2024-05-21 WILLIS-ALBRIGO Def DFP",19,"RFP"],
         ["2024-05-21 WILLIS-ALBRIGO Def Srogs",17,"SPROG"],
         ["BLAHA - Def City's RFP to PF",10,"RFP"],
         ["BLAHA - Def City's SROGS to PF",15,"SPROG"],
         ["City's RFP to PF, Set 1",17,"RFP"],
         ["City's SPROGS to PF, Set 1",34,"SPROG"],
         ["DISC RFA #1",21,"RFA"],
         ["DISC RFP #1",20,"RFP"],
         ["DISC SPROGS #1",35,"SPROG"],
         ["REQ FOR ADM (Set One) v.1",10,"RFA"],
         ["REQ for PRODUCTION (Set One) v.1 ",53,"RFP"],
         ["RTP#1 TO LINDA",18,"RFP"],
         ["SI#1 TO LINDA",39,"SPROG"],
         ["SROGS Set one",34,"SPROG"]]


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