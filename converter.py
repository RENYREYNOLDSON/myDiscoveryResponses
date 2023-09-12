###### CONVERTER
###### PROGRAM WRITTEN BY - Adam Reynoldson reynoldson2002@gmail.com FOR Darren Reid via UpWork 2023
######
###### Code for reading/saving the 'Discovery Responses'
######


### FUNCTIONS
########################################################################################################

from functions import *
import PyPDF2 as pdf
import re
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml.xmlchemy import OxmlElement
from docx.shared import Pt
from pdfminer.high_level import extract_text
import fitz
from boxdetect.pipelines import get_checkboxes
from boxdetect import config
from boxdetect.pipelines import get_boxes
import cv2


### CONSTANTS
########################################################################################################

FORM_VALUES = ["(1)","(2)",'1.1', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10', '2.11', '2.12', '2.13', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '4.1', '4.2', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '7.1', '7.2', '7.3', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '9.1', '9.2', '10.1', '10.2', '10.3', '11.1', '11.2', '12.1', '12.2', '12.3', '12.4', '12.5', '12.6', '12.7', '13.1', '13.2', '14.1', '14.2', '15.1', '16.1', '16.2', '16.3', '16.4', '16.5', '16.6', '16.7', '16.8', '16.9','16.10', '17.1', '20.1', '20.2', '20.3', '20.4', '20.5', '20.6', '20.7', '20.8', '20.9','20.10', '20.11', '50.1', '50.2', '50.3', '50.4', '50.5', '50.6']


### FUNCTIONS
########################################################################################################

# Adds paragraph after current
def insert_paragraph_after(paragraph, text=None, style=None):
    """Insert a new paragraph after the given paragraph."""
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        new_para.add_run(text)
    if style is not None:
        new_para.style = style
    return new_para

# Deletes a paragraph
def delete_paragraph(paragraph):
    p = paragraph._element
    if p!=None:
        p.getparent().remove(p)
        paragraph._p = paragraph._element = None



### READ THE PDF
########################################################################################################

#Reads a pdf use pdfreader
def readPDF(file):
    reader = pdf.PdfReader(file)# Create reader object
    #print(reader.get_fields())
    text=[]# Get each page
    for i in reader.pages:
        text.append(i.extract_text())
    text = "".join(list(text))
    return text


#Reads a pdf using fitz
def readPDF3(file):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        #REMOVE VERTICAL TEXT!!
        for block in page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]:
            for line in block["lines"]:
                wdir = line["dir"]    # writing direction = (cosine, sine)
                if wdir[0] == 0:  # either 90° or 270°
                    page.add_redact_annot(line["bbox"])
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)  # remove text, but no image
        #ADD TEXT
        text+=page.get_text()
    return text



### READ FROGs FORM
########################################################################################################
def readForm(file):
    cfg = config.PipelinesConfig()
    # important to adjust these values to match the size of boxes on your image
    cfg.width_range = (10,30)
    cfg.height_range = (10,30)
    # the more scaling factors the more accurate the results but also it takes more time to processing
    # too small scaling factor may cause false positives
    # too big scaling factor will take a lot of processing time
    cfg.scaling_factors = [1.3]
    # w/h ratio range for boxes/rectangles filtering
    cfg.wh_ratio_range = (0.3, 2)
    # group_size_range starting from 2 will skip all the groups
    # with a single box detected inside (like checkboxes)
    cfg.group_size_range = (1, 1)
    # num of iterations when running dilation tranformation (to engance the image)
    cfg.dilation_iterations = 0

    results=[]
    vals=[]
    f = fitz.open(file)
    for page in f:
        img = page.get_pixmap()
        img.save("assets/out.png")
        #SPLIT INTO COLUMNS
        img = cv2.imread("assets/out.png")
        height = img.shape[0]
        width = img.shape[1]

        # Cut the image in half
        width_cutoff = width // 2
        s1 = img[:, :width_cutoff]
        s2 = img[:, width_cutoff:]

        cv2.imwrite("assets/s1.png", s1)
        cv2.imwrite("assets/s2.png", s2)

        checkboxes1 = get_checkboxes("assets/s1.png", cfg=cfg, px_threshold=0.1, plot=False, verbose=False)
        checkboxes2 = get_checkboxes("assets/s2.png", cfg=cfg, px_threshold=0.1, plot=False, verbose=False)
        for checkboxes in [checkboxes1,checkboxes2]:
            #GET TRUE OF FALSE FOR CHECKBOXES ON THE PAGE
            for check in checkboxes:
                #Get array
                array = check[2]
                total=0
                for row in array[1:-1]:
                    total+=sum(row[1:-1])/len(row[1:-1])
                total = total/len(array[1:-1])
                vals.append(total)
                if total>=20:
                    results.append(True)
                else:
                    results.append(False)
    output=[]
    print(len(results))
    print(len(FORM_VALUES))
    for i in range(len(FORM_VALUES)):
        if results[i]==True:
            output.append(FORM_VALUES[i])
    return output





### FILTER THROUGH THE PDF
########################################################################################################
# Get requests and details from a pdf text string
def filterPDF(data):
    #Search Terms
    terms=["REQUESTNO.","INTERROGATORYNO.","ANDNO.","ENTSNO.","ONSNO.","TIONNO."]
    reqs=[]
    req=""
    adding=False
    split = data.split("\n")

    ####################### MAIN LOOP

    # Document vars
    case_number=""
    county=""
    plaintiff=""
    defendant=""
    document=""

    from_split =  re.split("([1-9]+\.[0-9]+)",data.replace("\n",""))
    #print(from_split)
    for i in range(len(split)):
        check=2

        #DOCUMENT DETAILS!!!!!!!!!!!!!!!!!!!!

        if adding==False:#THIS KEEPS THE OBJECTS IN ORDER AND COLLECTING PROPERLY!
            check=1
            #Get extra data here:
            if "CASENO." in split[i].replace(" ","").upper() and case_number=="":# Case Number & Document
                case_number = split[i].upper().split("NO.")[1].replace(" ","").replace(":","")
                #Get Document until can't
                c=1
                bypass=True
                while bypass or ("ASSIGNEDTO" not in split[i+c].replace(" ","").upper() and "CUTOFF:" not in split[i+c].upper() and "PLACE:" not in split[i+c].upper() and "FILED:" not in split[i+c].upper() and "DATE:" not in split[i+c].upper() and c<20 and "PROPOUNDINGPARTY:" not in split[i+c].replace(" ","")):
                    val = min(max(0,len(split[i+c])-1),10)
                    if val>2:
                        if split[i+c][:val]==split[i+c][:val].upper() or bypass==False:
                            document = document + split[i+c]
                            bypass=False
                    c+=1

            elif "COUNTY" in split[i].replace(" ","") and county=="":# County
                county = split[i].split("COUNTY OF",1)[-1]
                c=1
                #Get County until can't
                while split[i+c].replace(" ","").replace("\n","")!="" and split[i+c]==split[i+c].upper() and c<10:
                    county=county+split[i+c]
                    c+=1

            elif "PROPOUNDINGPARTY:" in split[i].replace(" ","") and plaintiff=="":#Plaintiff and defendant
                #Add until not propounding party
                plaintiff=split[i].split(":")[-1]
                c=1
                while "SETNUMBER" not in split[i+c].replace(" ","") and "SETNO" not in split[i+c].replace(" ","")  and c<20:
                    if defendant=="":# If adding to plaintiff
                        if "RESPONDINGPARTY:" in split[i+c].replace(" ",""):
                            defendant = split[i+c].split(":")[-1]
                        else:
                            plaintiff = plaintiff + split[i+c]
                    else:
                        defendant = defendant + split[i+c]
                    c+=1

        #Clean Plaintiff and defendant
        plaintiff = plaintiff.upper().replace("DEFENDANT","").replace("(S)","")
        done = False
        for i2 in range(len(plaintiff)):
            if done==False:
                if plaintiff[i2].isalpha():
                    plaintiff = plaintiff[i2:]
                    done = True

        defendant = defendant.upper().replace("PLAINTIFF","").replace("(S)","")
        done = False
        for i2 in range(len(defendant)):
            if done==False:
                if defendant[i2].isalpha():
                    defendant = defendant[i2:]
                    done = True

        #SWAP THEM!!! TEMP
        temp = plaintiff
        plaintiff = defendant
        defendant = temp

        #GET REQUESTS!!!!!!!!!!!!!!!!!!!!

        if any(t in split[i].replace(" ","") for t in terms):# If request term used
            adding=True
            if req!="":
                reqs.append(req.strip())
            req=""
        elif "1. "==split[i][:3]:#Restart requests
            reqs=[]
            adding=True
            req = split[i].split(".",1)[1]
        elif str(len(reqs)+check)+". " in split[i][:10]:# If basic numbering used
            adding=True
            if req!="":
                reqs.append(req.strip())
            req = split[i].split(".",1)[1]
        elif adding==True:# Add the request text 
            if "DATED:" in split[i].replace(" ","")[:10].upper():
                adding = False
            elif len(split[i].replace(" ",""))>2 and not(split[i].replace(" ","")==split[i].replace(" ","").upper() and  "." not in split[i]):
                req = req+" "+split[i].strip()
        #print(split[i])

    #ISSUE end of each page continues to the margin text!

    reqs.append(req.strip())
    #######################
    #Get type of discovery
    req_type=""
    search = data[:1000].replace(" ","")# Search 1st 1000 chars
    if "INTERROGATORIES" in search:
        req_type="SPROG"
    elif "ADMISSIONS" in search:
        req_type="RFA"
    else:
        req_type="RFP"
    
    """
    print("CASE: "+str(case_number))
    print("DOCUMENT: "+str(document))
    print("COUNTY: "+str(county))
    print("Plaintiff: "+str(plaintiff))
    print("Defendant: "+str(defendant))
    """

    details = {"case_number":case_number,
                "document":document,
                "county":county,
                "plaintiff":plaintiff,
                "defendant":defendant,
                "date":""}

    return reqs,req_type,details


### COMBINE ALL INTO GETREQUESTS
########################################################################################################
# Get the requests and filter
def getRequests(file):
    #If a form interrogatory
    data = readPDF3(file)
    backup_data = readPDF(file)
    if "DISC-001" in data.replace(" ","")[:5000]:
        reqs = readForm(file)
        reqs_type = "FROG"
        details = {"case_number":"",
                    "document":"",
                    "county":"",
                    "plaintiff":"",
                    "defendant":""}
    else:
        reqs,reqs_type,details = filterPDF(data)
        breqs,breqs_type,bdetails = filterPDF(backup_data)
        for i in range(len(reqs)):
            if reqs[i]=="":
                reqs[i]=breqs[i]
    return reqs,reqs_type,details


### UPLOAD THE DOCS
########################################################################################################
# Save requests, responses and details to a word DOCX
def updateDOC(reqs,resps,details,file,name,numbers):
    templates = {
    "RFA":"assets/Response to RFA.docx",
    "RFP":"assets/Response to RFP.docx",
    "SPROG":"assets/Response to SROG.docx",
    "FROG":"assets/Response to FROG2.docx"
    }
    #Loading template file
    file=templates[file]
    doc = Document(file)
    #Normal Style
    if "FROG" in file:
        style = doc.styles["Normal"]
        font = style.font
        font.name = "Times New Roman"
        font.size = Pt(12)
    else:
        style = doc.styles['Normal']
        font = style.font
        font.size = Pt(12)
    # 1. ADD THE DETAILS

    #FOOTER
    for section in doc.sections:
        footer=section.footer
        footer.paragraphs[1].text  = footer.paragraphs[1].text.replace("DOCUMENTX", details["document"])
    #TABLE TEXT
    #First Column
    table = doc.tables[0].row_cells(0)
    for p in table[0].paragraphs:
        text = str(p.text)
        text=text.replace("PLAINTIFFX",details["plaintiff"])
        text=text.replace("DEFENDANTX",details["defendant"])
        p.text = text
    #Second column
    for p in table[1].paragraphs:
        text = str(p.text)
        if "CASENUMBERX" in text:
            #text=text.replace("CASE NUMBERX",details["case_number"])
            p.text=""
            run = p.add_run("Case No. "+str(details["case_number"]))
            run.bold=True
        elif "DOCUMENTX" in text:
            p.text=""
            run = p.add_run("PLAINTIFF'S RESPONSES TO "+str(details["document"]))
            run.bold=True
    #GENERAL TEXT
    for p in doc.paragraphs:
        text = str(p.text)
        if "PLAINTIFFX" in text or "DEFENDANTX" in text or "DOCUMENTX" in text:
            text=text.replace("PLAINTIFFX",details["plaintiff"])
            text=text.replace("DEFENDANTX",details["defendant"])
            text=text.replace("DOCUMENTX",details["document"])
            p.text = text
        if "NAME OF COUNTYX" in text:
            p.text=""
            run = p.add_run(text.replace("NAME OF COUNTYX",details["county"]))
            run.bold=True


    # 2. ADD THE REQUEST RESPONSES
    if "FROG" in file:# Use the 'numbers' list for this
        add_next = False
        counter=0
        for p in doc.paragraphs:
            if "NO. " in p.text:
                if counter<len(numbers):#If still valid
                    if str(numbers[counter]) in p.text:
                        insert_paragraph_after(p,"           "+reqs[counter],"Normal")#Add req
                        add_next = True
                    else:
                        delete_paragraph(p)
                else:#If finished
                    delete_paragraph(p)
            elif "RESPONSE:" in p.text:
                if add_next:#Add new para
                    insert_paragraph_after(p,"           "+resps[counter],"Normal")#Add req
                    counter+=1
                    add_next = False
                else:#Delete this
                    delete_paragraph(p)
    else:
        counter=0
        for p in doc.paragraphs:
            if "NO. " in p.text:
                if counter<len(reqs):
                    if "RESPONSE" not in p.text:
                        insert_paragraph_after(p,"           "+reqs[counter],"Normal")
                    else:
                        insert_paragraph_after(p,"           "+resps[counter],"Normal")
                        counter+=1
                else:
                    #Destroy para
                    if "RESPONSE" not in p.text:
                        delete_paragraph(prev_p)
                    delete_paragraph(p)
            prev_p = p
    doc.save(str(name)+".docx")






