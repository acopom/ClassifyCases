#import pathlib
#import textwrap
import google.generativeai as genai

import requests
#import genai

#import vertexai
#from vertexai.preview.generative_models import GenerativeModel, Part

import time
#import requests

import json


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
        qtext +" Then, answer the following question: are there the term Cataract found in the document? Please answer yes, no or no information.",
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
        qtext +" Then, answer the following question: how many years ago did the patient take optical examination. Please answer years only numerically. If there is no information about it, answer null",
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
        qtext+ " Then, answer the following question: how old is the patient? Please answer age only numerically. If there is no information, answer no information.",
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
        qtext+ " Then, answer the following question: how many cataract diagnosis in the document? Please answer the number only."
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


def step9(qtext: str, model):
    response = model.generate_content(
        qtext +" Then, answer the following question: are there the term Cataract found in the document? Please answer yes, no or no information.",
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
        qtext+ " Then, answer the following question: how old is the patient. Please answer age only numerically. If there is no information, please answer no information",
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

# read json file
f = open('./cataract.maru.json', 'r')
json_dict = json.load(f)


for pmid, dict_ti_ab in json_dict.items():
    title = dict_ti_ab['Title']
    abstract = dict_ti_ab['Abstract']
    model = genai.GenerativeModel('gemini-pro')
    print(pmid)
    print("title: " + title)
    print("abstract: " + abstract)
    print("Step2")
    step2(abstract, model)    
