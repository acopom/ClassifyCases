#import pathlib
#import textwrap
import google.generativeai as genai

import requests
#import genai

#import vertexai
#from vertexai.preview.generative_models import GenerativeModel, Part

import time
#import requests


def step2(qtext: str, model):
    response = model.generate_content(
       "Does the patient have cataract surgery? Please answer yes, no, or no information.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    #print(response.text)
    if 'Yes' in str(restext) or 'yes' in str(restext):
      print("Step10")
      step10(qtext, model)
    elif 'No' in str(restext) or 'no' in str(restext):
      print("Step3")
      step3(qtext, model)
    elif 'access' in str(restext):
      print("Try again")
      time.sleep(3)
      step2(qtext, model)
    else:
      print(" is an exception")

def step3(qtext: str, model):
    response = model.generate_content(
        qtext +" Then, answer the following question: was the patient diagnosed with cataract? Please answer yes, no, or no information.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if 'Yes' in str(restext) or 'yes' in str(restext) :
      print("Step8")
      step8(qtext, model)
    elif 'No' in str(restext) or 'no' in str(restext) :
      print("Step4")
      step4(qtext, model)
    elif 'access' in str(restext) :
      print("Try again")
      time.sleep(3)
      step3(qtext, model)
    else:
      print(" is an exception")
      
def step4(qtext: str, model):
    response = model.generate_content( 
        qtext +" Then, answer the following question: was the patient diagnosed with congenital, traumatic or juvenile cataract? Please answer yes, no or no information.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if 'Yes' in str(restext) or 'yes' in str(restext) :
      print(" is excluded")
    elif 'No' in str(restext) or 'no' in str(restext) :
      print("Step5")
      step5(qtext, model)
    elif 'access' in str(restext) :
      print("Try again")
      time.sleep(3)
      step4(qtext, model)
    else:
      print(" is an exception")

def step5(qtext: str, model):
    response = model.generate_content(
        qtext +" Then, answer the following question: are there the term Cataract found in the document? Please answer yes, or no.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if 'Yes' in str(restext) or 'yes' in str(restext) :
      print("excluded")
    elif 'No' in str(restext) or 'no' in str(restext) :
      print("Step6")
      step6(qtext, model)
    elif 'access' in str(restext) :
      print("Try again")
      time.sleep(3)
      step5(qtext, model)
    else:
      print("an exception")
      
def step6(qtext: str, model):
    response = model.generate_content(
        qtext +" Then, answer the following question: how many years ago did the patient take optical examination. Please answer years only numerically. If there is no information about it, answer -1",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)    
    if 'access' in str(restext) :
      print('Try again')
      time.sleep(3)
      step6(qtext, model)
    elif is_int(restext):
      if int(restext) > 4 :
        print( 'excluded')
      elif int(restext) < 5 :
        print("Step7")
        step7(qtext, model)
    else:
      print("an exception")
      
def step7(qtext: str, model):
    response = model.generate_content(
        qtext+ " Then, answer the following question: how old is the patient? Please answer age only numerically. Please answer the age only numerically. If there is no information about the age of the patient, please answer -1.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)    
    if 'access' in str(restext) :
      print('Try again')
      time.sleep(3)
      step10(qtext, model)
    if is_int(restext):
      if int(restext) > 49 :
        print(' is a control')
      elif int(restext) < 50 :
        print(' is excluded')
    else:
      print( " is an exception")


def step8(qtext: str, model):
    response = model.generate_content(
        qtext+ " Then, answer the following question: how many cataract diagnosis are there in the document? Please answer the number only. If there is no information about the number, please answer -1."
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if is_int(restext):
      if int(restext) >= 2 : 
        print("Step10")
        step10(qtext, model)
      else :
        print("Step9")
        step9(qtext, model)
    else :
      print( " is an exception")      

def step9(qtext: str, model):
    response = model.generate_content(
        qtext +" Then, answer the following question: are there the term Cataract found in the document? Please answer yes or no.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if 'Yes' in str(restext) or 'yes' in str(restext) :
      print("Step10")
      step10(qtext, model)
    elif 'No' in str(restext) or 'no' in str(restext) :
        print(' is excluded')
    elif 'access' in str(restext) :
      print("Try again")
      time.sleep(3)
      step5(qtext, model)
    else:
      print("an exception")

def step10(qtext: str, model):
    response = model.generate_content(
        qtext+ " Then, answer the following question: how old is the patient. Please answer the age only numerically. If there is no information about the age of the patient, please answer -1.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if 'access' in str(restext) :
      print('Try again')
      time.sleep(3)
      step10(qtext, model)
    elif is_int(restext):
      if int(restext) > 49 :
        print(' is a case')
      elif int(restext) < 50 :
        print(' is excluded')
    else:
      print( " is an exception")

def is_int(istr:str):
    try:
        int(istr)
    except ValueError:
        return False
    else:
        return True
    

def multi2text(candidates):
    content = candidates[0].content
    resstr = "";
    for part in content.parts:
        text = part.text
        resstr +=  text
    return resstr
    
genai.configure(api_key="xxx")

dlist = [
  #pmid
'31391702',
'31332133',
'31146719',
'30900600',
'30890130',
'30882657',
'30640280',
'30606142',
'30605941',
'30605939',
'30567140',
'30181404',
'30157798',
'30029635',
'29970067',
'29786001',
'29549136',
'29450372',
'29044088',
'28974839',
'28751510',
'28746174',
'28723783',
]

ulist = [
  #pmc urls
]


for pmid in dlist:
#for docuri in ulist:    
    r = requests.get("http://togows.org/entry/ncbi-pubmed/"+pmid+"/abstract")
    #abstxt = r.text
    #r = requests.get("https://pubmed.ncbi.nlm.nih.gov/"+pmid+"/")
    model = genai.GenerativeModel('gemini-pro')
    #print(dir(model))
    #model.process_html(r)
    #qtext = ""
    qtext = "Read the gievn abstract: " + r.text
    #qtext = "Read the following paper with url: " + docuri  
    print(pmid)
    print("Step2")
    step2(qtext, model)
