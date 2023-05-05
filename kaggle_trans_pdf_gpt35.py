!pip install pypdf nltk openai files
from pypdf import PdfReader
from nltk.tokenize import sent_tokenize
import requests
import openai
import nltk
import time
import files
​
​
res = requests.get('https://www.gefahrgutberatung.ch/wp-content/uploads/2021/01/IMDG-Code-40-20-1.pdf')
​
with open('IMDG-Code-40-20-1.pdf','wb') as f:
  f.write(res.content)
pdf_name= "IMDG-Code-40-20-1.pdf"
reader = PdfReader(pdf_name)
number_of_pages = len(reader.pages)
chunks =[]
//  使用你自己的chatgpt的api
TOKEN = ''
//
openai.api_key = TOKEN
nltk.download('punkt')
for i in range(number_of_pages):
  page = reader.pages[i]
  text = page.extract_text()
  sentences = sent_tokenize(text)
  input_sentences = ''
  
  for sentence in sentences:
   input_sentences += sentence
   if len(input_sentences) > 1000:
    chunks.append(input_sentences)
    input_sentences = ''
  chunks.append(input_sentences)
​
with open('output.txt', 'w') as f:
  f.write("imdg-code2020年版本 中英对照\n")
​
j=len(chunks)
print("共有部分:",len(chunks))
for i in range(1500,2000):
  
  time.sleep(20)
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "请帮忙翻译一下的文件成中文简体"},
        {"role": "user", "content": chunks[i]},
        
    ]
  )
  print("传输到部分：",i,chunks[i][0:20])
  with open('output.txt', 'a') as f:
    f.write("原文：" + chunks[i] + '\n')
    f.write("翻译结果：" + completion.choices[0].message.content + '\n')
​
​
files.download('output.txt')
