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
import copy
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml.xmlchemy import OxmlElement
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt
from pdfminer.high_level import extract_text
import fitz
from CTkMessagebox import CTkMessagebox
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
    doc = fitz.Document(file)
    text = ""
    for page in doc:
        """
        print(page.rect.width)
        crop_rect = fitz.Rect(300,0,page.rect.width,page.rect.height)
        page.set_mediabox(crop_rect)
        page.set_cropbox(crop_rect)
        page.set_trimbox(crop_rect)
        print(page)
        print(page.mediabox)
        """
        #REMOVE VERTICAL TEXT!!
        for block in page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]:
            for line in block["lines"]:
                wdir = line["dir"]    # writing direction = (cosine, sine)
                if wdir[0] == 0:  # either 90° or 270°
                    page.add_redact_annot(line["bbox"])
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)  # remove text, but no image
        

        text+=page.get_text()
        #print(page.rect.width)
    return text



### READ FROGs FORM
########################################################################################################
def readForm(file):
    try:
        cfg = config.PipelinesConfig()
        # important to adjust these values to match the size of boxes on your image
        cfg.width_range = (9,30)
        cfg.height_range = (9,30)
        # the more scaling factors the more accurate the results but also it takes more time to processing
        # too small scaling factor may cause false positives
        # too big scaling factor will take a lot of processing time
        cfg.scaling_factors = [1]
        # w/h ratio range for boxes/rectangles filtering
        cfg.wh_ratio_range = (0.8, 2.5)
        # group_size_range starting from 2 will skip all the groups
        # with a single box detected inside (like checkboxes)
        cfg.group_size_range = (1, 1)
        # num of iterations when running dilation tranformation (to engance the image)
        cfg.dilation_iterations = 0

        results=[]
        vals=[]
        f = fitz.open(file)
        page_count = 0#Used to add extra results when scanning fails
        for page in f:
            img = page.get_pixmap()
            img.save(os.path.join(os.path.dirname(__file__),"assets/out.png"))
            #SPLIT INTO COLUMNS
            img = cv2.imread(os.path.join(os.path.dirname(__file__),"assets/out.png"))
            height = img.shape[0]
            width = img.shape[1]

            # Cut the image in half
            width_cutoff = int(width // 2.5)
            s1 = img[:, :width_cutoff]
            s2 = img[:, width_cutoff:]

            cv2.imwrite(os.path.join(os.path.dirname(__file__),"assets/s1.png"), s1)
            cv2.imwrite(os.path.join(os.path.dirname(__file__),"assets/s2.png"), s2)

            checkboxes1 = get_checkboxes(os.path.join(os.path.dirname(__file__),"assets/s1.png"), cfg=cfg, px_threshold=0.1, plot=False, verbose=False)
            checkboxes2 = get_checkboxes(os.path.join(os.path.dirname(__file__),"assets/s2.png"), cfg=cfg, px_threshold=0.1, plot=False, verbose=False)
            for checkboxes in [checkboxes1,checkboxes2]:
                #GET TRUE OF FALSE FOR CHECKBOXES ON THE PAGE
                for check in checkboxes:
                    #Get array
                    array = check[2]
                    total=0
                    for row in array[2:-4]:
                        total+=sum(row[2:-4])/len(row[2:-4])
                    total = total/len(array[2:-4])
                    vals.append(total)
                    if total>=20:
                        results.append(True)
                    else:
                        results.append(False)
            if page_count==0 and len(results)==0:
                results.append(False)
        output=[]
        print(len(results))
        print(len(FORM_VALUES))
        for i in range(len(FORM_VALUES)):
            if results[i]==True:
                output.append(FORM_VALUES[i])
    except:
        msg = CTkMessagebox(title="Could not load FROG", message="The FROG file could not be read correctly. Defaulted to using all discovery requests.",
                            icon="warning", option_1="Okay",corner_radius=0)
        output = FORM_VALUES.copy()
    return output










### FILTER THROUGH THE PDF
########################################################################################################
# Get requests and details from a pdf text string
def filterPDF(data):
    #Search Terms
    terms=["REQUESTNO.","INTERROGATORYNO.","ANDNO.","ENTSNO.","ONSNO.","TIONNO.","REQUESTFORADMISSION"]
    reqs=[]
    keys=[]
    req=""
    adding=False
    term_used=False
    hard_stop=False
    start_at_one=True
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

        try:
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
        except:
            pass
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
        if not hard_stop:
            print("Next")
            print(split[i])
            if any(t in split[i].replace(" ","").upper() for t in terms) and (split[i].replace(" ","")[-1] in [":","."] or split[i].replace(" ","")[-1].isdigit()):#       If request term used, must end in a certain character or a number, in case it is in text. Could check split length?
                #Add the custom key
                print(split[i])
                key =re.findall(r'\d+', split[i][10:])[0]
                if start_at_one==False or (term_used==False and key!="1"):
                    keys.append(key)
                    start_at_one=False
                adding=True
                if req!="":
                    reqs.append(req.strip())
                req=""
                if not term_used:
                    reqs=[]
                term_used=True
                
            elif "1. "==split[i][:3] and term_used==False:#                                    Restart requests
                reqs=[]
                adding=True
                req = split[i].split(".",1)[1]
            elif str(len(reqs)+check)+"." in split[i][:10] and term_used==False:#            If basic numbering used
                adding=True
                if req!="":
                    reqs.append(req.strip())
                req = split[i].split(".",1)[1]
            elif adding==True:#                                         Add the request text 
                if any(end in split[i].replace(" ","")[:10].upper() for end in ["DATED:","DATEDTHIS"]):
                    adding = False
                    hard_stop=True#Used to stop scanning for reqs
                elif len(split[i].replace(" ",""))>2 and not(split[i].replace(" ","")==split[i].replace(" ","").upper() and len(split[i].replace(" ",""))>15 and split[i][-1].replace(" ","").strip() not in [".","?"]):
                    req = req+" "+re.sub(r"-[ 0-9 ]-","",split[i].strip().replace("///",""))

    #Stop reading numbers in margin
    #Stop reading side text




    #ISSUE end of each page continues to the margin text!

    reqs.append(req.strip())
    #######################
    #Get type of discovery
    req_type=""
    search = data[:1000].replace(" ","")# Search 1st 1000 chars
    if "INTERROGATOR" in search:
        req_type="SPROG"
    elif "ADMISSION" in search:
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

    return reqs,req_type,details,keys


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
                    "defendant":"",
                    "date":""}
        keys=[]
    else:
        reqs,reqs_type,details,keys = filterPDF(data)
        """
        breqs,breqs_type,bdetails,keys = filterPDF(backup_data)
        for i in range(len(reqs)):
            if reqs[i]=="":
                reqs[i]=breqs[i]
        """
    return reqs,reqs_type,details,keys


### UPLOAD THE DOCS
########################################################################################################
# Save requests, responses and details to a word DOCX
def updateDOC(reqs,resps,details,firm_details,file,name,numbers):
    templates = {
    "RFA":"assets/Response to RFA.docx",
    "RFP":"assets/Response to RFP.docx",
    "SPROG":"assets/Response to SROG.docx",
    "FROG":"assets/Response to FROG2.docx"
    }
    headings = {
    "RFA":"REQUEST FOR ADMISSION",
    "RFP":"DEMAND",
    "SPROG":"SPECIAL INTERROGATORY",
    "FROG":"FORM INTERROGATORY"
    }
    #Select the correct heading for the file
    if isinstance(file,str):
        heading=headings[file]
        #Loading template file
        filename=os.path.join(os.path.dirname(__file__),templates[file])
    else:#If a list of types (for export with client), set headings later
        filename=os.path.join(os.path.dirname(__file__),templates["RFA"])
    doc = Document(filename)
    #Normal Style
    if "FROG" in filename:
        style = doc.styles["Normal"]
        font = style.font
        font.name = "Times New Roman"
        font.size = Pt(12)
    else:
        style = doc.styles['Normal']
        font = style.font
        font.size = Pt(12)
    #Heading style
    style = doc.styles.add_style('Heading', WD_STYLE_TYPE.PARAGRAPH)
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(12)
    font.bold=True
    font.underline=True

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
        if (x in text for x in ["PLAINTIFFX","DEFENDANTX","DOCUMENTX","DATEX","ATTORNEYSX","FIRM_NAMEX","ADDRESS_LINE_1X","ADDRESS_LINE_2X","TELEPHONEX","FACSIMILEX","EMAILX"]):
            #Normal Details
            text=text.replace("PLAINTIFFX",details["plaintiff"])
            text=text.replace("DEFENDANTX",details["defendant"])
            text=text.replace("DOCUMENTX",details["document"])
            text=text.replace("DATEX",details["date"])
            #Firm Details
            text=text.replace("ATTORNEYSX",firm_details["attorneys"])
            text=text.replace("FIRM_NAMEX",firm_details["firm_name"])
            text=text.replace("ADDRESS_LINE_1X",firm_details["address_line_1"])
            text=text.replace("ADDRESS_LINE_2X",firm_details["address_line_2"])
            text=text.replace("TELEPHONEX",firm_details["telephone"])
            text=text.replace("FACSIMILEX",firm_details["facsimile"])
            text=text.replace("EMAILX",firm_details["email"])
            p.text = text
        if "NAME OF COUNTYX" in text:
            p.text=""
            run = p.add_run(text.replace("NAME OF COUNTYX",details["county"]))
            run.bold=True


    # 2. ADD THE REQUEST RESPONSES
    counter=0
    started=False
    for p in doc.paragraphs:
        if "STARTX" in p.text:
            started=True
            delete_paragraph(p)
        if started:
            for i in range(len(reqs)):#Add each paragraph with it's own correct heading
                if not isinstance(file,str):
                    heading = headings[file[counter]]
                #Add heading
                prev_p = insert_paragraph_after(prev_p,heading+" NO. "+str(numbers[counter])+":","Heading")
                #Add request
                prev_p = insert_paragraph_after(prev_p,"           "+reqs[counter],"Normal")
                #Add heading
                prev_p = insert_paragraph_after(prev_p,"RESPONSE TO "+heading+":","Heading")
                #Add response
                prev_p = insert_paragraph_after(prev_p,"           "+resps[counter],"Normal")
                #Next
                counter+=1
            doc.save(str(name)+".docx")
            return
        prev_p = p






### READ CLIENT FEEDBACK
########################################################################################################
def read_client_feedback(filename):
    #Read client feedback from a DOCX file
    #Given this filename, open, get data into sections. Send to main program to update requests
    #Each one needs key,resp,type
    #EXAMPLE FORMAT: feedback=[{"key":"1","type":"RFA","response":"CLIENT FEEDBACK: incredible"}]
    feedback=[]
    doc = Document(filename)
    #Get each key from the request
    #Then find the response and add to a new dict
    current_key=""
    current_type=""
    current_response=""
    for p in doc.paragraphs:
        #RFA
        if "REQUEST FOR ADMISSION NO. " in p.text:
            if current_response!="":
                feedback.append({"key":current_key,"type":current_type,"response":"CLIENT FEEDBACK: "+str(current_response)})
            current_key = ".".join(re.findall(r'\d+', p.text))
            current_type = "RFA"
        elif "RESPONSE TO REQUEST FOR ADMISSION:" in p.text or "RESPONSE TO DEMAND:" in p.text or "RESPONSE TO SPECIAL INTERROGATORY:" in p.text or "RESPONSE TO FORM INTERROGATORY:" in p.text:
            current_response = ""
        #RFP
        elif "DEMAND NO. " in p.text:
            if current_response!="":
                feedback.append({"key":current_key,"type":current_type,"response":"CLIENT FEEDBACK: "+str(current_response)})
            current_key = ".".join(re.findall(r'\d+', p.text))
            current_type = "RFP"
        #SPROG
        elif "SPECIAL INTERROGATORY NO. " in p.text:
            if current_response!="":
                feedback.append({"key":current_key,"type":current_type,"response":"CLIENT FEEDBACK: "+str(current_response)})
            current_key = ".".join(re.findall(r'\d+', p.text))
            current_type = "SPROG"
        #FROG
        elif "FORM INTERROGATORY NO. " in p.text or "Dated:" in p.text[:8]:
            if current_response!="":
                feedback.append({"key":current_key,"type":current_type,"response":"CLIENT FEEDBACK: "+str(current_response)})
            current_key = ".".join(re.findall(r'\d+', p.text))
            current_type = "FROG"
        else:
            current_response = current_response + p.text#Add current paragraph
    return feedback




##SHOULD ADD THREADS FOR BOX DETECT!