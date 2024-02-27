import pathlib
import textwrap
import google.generativeai as genai

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

import time
import requests

def step2(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract: "+ abstxt + " Answer the question that does the patient have cataract surgery? Please answer yes, no, or no information.",
    )
    print(response.text)
    if 'Yes' in str(response.text) or 'yes' in str(response.text):
      print("Step10")
      step10(abstxt, model)
    elif 'No' in str(response.text) or 'no' in str(response.text):
      print("Step3")
      step3(abstxt, model)
    elif 'access' in str(response.text):
      print("Try again")
      time.sleep(3)
      step2(abstxt, model)
    else:
      print(" is an exception")

def step3(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract: "+ abstxt +" Answer the question that does the patient was diagnosed with cataract? Please answer yes, no, or no information.",
    )
    print(response.text)
    if 'Yes' in str(response.text) or 'yes' in str(response.text) :
      print("Step8")
      step8(abstxt, model)
    elif 'No' in str(response.text) or 'no' in str(response.text) :
      print("Step4")
      step4(abstxt, model)
    elif 'access' in str(response.text) :
      print("Try again")
      time.sleep(3)
      step3(abstxt, model)
    else:
      print(" is an exception")
      
def step4(abstxt: str, model):
    response = model.generate_content( 
        "Read the following abstract: "+ abstxt +" Answer the question that is any exclusion DX code found. Please answer yes, no or no information.",
    )
    print(response.text)
    if 'Yes' in str(response.text) or 'yes' in str(response.text) :
      print(" is excluded")
    elif 'No' in str(response.text) or 'no' in str(response.text) :
      print("Step5")
      step5(abstxt, model)
    elif 'access' in str(response.text) :
      print("Try again")
      time.sleep(3)
      step4(abstxt, model)
    else:
      print(" is an exception")

def step5(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract: "+ abstxt +" Answer the question that are NLP or ICR Cataract found. Please answer yes, no or no information.",
    )
    print(response.text)
    if 'Yes' in str(response.text) or 'yes' in str(response.text) :
      print("excluded")
    elif 'No' in str(response.text) or 'no' in str(response.text) :
      print("Step6")
      step6(abstxt, model)
    elif 'access' in str(response.text) :
      print("Try again")
      time.sleep(3)
      step5(abstxt, model)
    else:
      print("an exception")
      
def step6(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract: "+ abstxt +" Answer the question that how long does the patient have optical exam. Please answer years only numerically. If there is no information about it, answer null",
    )
    print(response.text)    
    if 'access' in str(response.text) :
      print('Try again')
      time.sleep(3)
      step6(abstxt, model)
    elif is_int(response.text):
      if int(response.text) > 4 :
        print( 'excluded')
      elif int(response.text) < 5 :
        print("Step7")
        step7(abstxt, model)
    else:
      print("an exception")
      
def step7(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract:" + abstxt+ " Answer the question how old is the patient. Please answer age only numerically. If there is no information, answer no.",
    )
    print(response.text)    
    if 'access' in str(response.text) :
      print('Try again')
      time.sleep(3)
      step10(abstxt, model)
    if is_int(response.text):
      if int(response.text) > 49 :
        print(' is a control')
      elif int(response.text) < 50 :
        print(' is excluded')
    else:
      print( " is an exception")


def step8(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract:" + abstxt+ " Answer the question how many DX codes are there. Please answer the number only."
    )
    print("Step10")
    step10(abstxt, model)

def step9(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract: "+ abstxt +" Answer the question that are NLP or ICR Cataract found. Please answer yes or no."
    )
    print(response.text)
    if 'Yes' in str(response.text) or 'yes' in str(response.text) :
      print("Step10")
      step10(abstxt, model)
    elif 'No' in str(response.text) or 'no' in str(response.text) :
        print(' is excluded')
    elif 'access' in str(response.text) :
      print("Try again")
      time.sleep(3)
      step5(abstxt, model)
    else:
      print("an exception")

def step10(abstxt: str, model):
    response = model.generate_content(
        "Read the following abstract:" + abstxt+ " Answer the question how old is the patient. Please answer age only numerically.",
    )
    candidates = response.candidates
    restext = multi2text(candidates)
    print(restext)
    if 'access' in str(restext) :
      print('Try again')
      time.sleep(3)
      step10(abstxt, model)
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
    
genai.configure(api_key="AIzaSyBv61b6019I-FomMYQ0N4NYaREQ4K2k3R8")

dlist = [
    '38239417',
    '38068917',
    '37904374',
    '37899280',
]

for pmid in dlist:
    r = requests.get("http://togows.org/entry/pubmed/"+docuri+"/abstract")
    abstxt = r.text
    model = genai.GenerativeModel('gemini-pro')
    print(docuri)
    print("Step2")
    step2(abstxt, model)
