import pandas as pd
import numpy as np
from . import review
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time
import random
import re
import pickle
from konlpy.tag import Okt
import tensorflow as tf
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration


def get_reviews(url):
  subprocess.Popen(
      r'C:/Program Files/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/chrometemp"')
  options = Options()
  options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
  driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

  rv_df = pd.DataFrame(columns=['star','date','store','review','help'])
  driver.get(url)
  driver.implicitly_wait(4)
  time.sleep(1+random.randint(1, 5)/10)
  show_me_reviews = '#btfTab > ul.tab-titles > li:nth-child(2)'
  try:
    driver.find_element(By.CSS_SELECTOR, show_me_reviews).click() 
  except:
    pass
  time.sleep(1+random.randint(1, 5)/10)
  
  cnt = 0
  i = 2
  k = 0
  go = True
  while go:
      pageBtns = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{i}]'
      if i == 13: 
          i = 3
          pageBtns = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{i}]'
      try:
          driver.find_element(By.XPATH, pageBtns).click()
      except : 
          go = False
          driver.close()
      html = driver.page_source
      soup = BeautifulSoup(html, 'html.parser')
      data = soup.select(".sdp-review__article__list")
      i += 1
      for inx, one in enumerate(data):
          if len(one) > 8: 
              time.sleep(random.randint(1, 5)/10)
              rv = review.Review()   
              print(f'data 있음 {inx}')
              rv.star = int(one.select_one('.sdp-review__article__list__info__product-info__star-orange')['data-rating'])
              rv.date = one.select_one('.sdp-review__article__list__info__product-info__reg-date').get_text()
              try: rv.review = one.select('.sdp-review__article__list__headline')[0].text.strip() + ' '
              except: pass
              try: rv.review += one.select_one('.sdp-review__article__list__review').get_text().strip().replace('/n', ' ')
              except: pass
              try: rv.help = int(one.select_one('.js_reviewArticleHelpfulCount').get_text())
              except: pass
              cnt = 0
              rv_df.loc[k] = [rv.star, rv.date, rv.review, rv.help]
              if k == 19 : 
                go = False
                driver.close()
                break
              k += 1
          else:
              cnt += 1
              if cnt == 3:
                  i = 2
                  cnt = 0
                  go = False
                  driver.close()
 
  return rv_df
 

max_len = 200
model1 = tf.keras.models.load_model('./nlp/model1/okt_best_model.h5')
okt = Okt()
with open('./nlp/model1/tokenizer.pickle', 'rb') as handle:
    tokenizer1 = pickle.load(handle)
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

def tokenize(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    new_sentence = okt.morphs(new_sentence)
    new_sentence = [word for word in new_sentence if not word in stopwords]
    encoded = tokenizer1.texts_to_sequences([new_sentence])
    pad_new = tf.keras.preprocessing.sequence.pad_sequences(encoded, maxlen = max_len)
    return pad_new

def positive_or_negative(rv_df):
  pos_df = pd.DataFrame(columns=['star','date','store','review','help'])
  neg_df = pd.DataFrame(columns=['star','date','store','review','help'])
  for idx, t in enumerate(rv_df['review']):
    try:
      score = float(model1.predict(tokenize(t)))
      if score > 0.5 :
        pos_df = pos_df.append(rv_df.iloc[idx,:])
      else : 
        neg_df = neg_df.append(rv_df.iloc[idx,:])
    except : pass
      
  return pos_df, neg_df

tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")
  
def summarize_list(list):
  sents = ' '.join(list)
  input_ids = tokenizer.encode(sents, return_tensors="pt")

  summary_text_ids = model.generate(
      input_ids=input_ids,
      bos_token_id=model.config.bos_token_id,
      eos_token_id=model.config.eos_token_id,
      length_penalty=2.0,
      max_length=40,
      min_length=10,
      num_beams=4,
  )
  return tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
   
   
def summarize(pos_df, neg_df):
  p_sample = pos_df['review'].sample(frac=1, random_state=42)
  n_sample = neg_df['review'].sample(frac=1, random_state=42)
  
  pos_list = p_sample.tolist()
  neg_list = n_sample.tolist()
    
  result_pos = summarize_list(pos_list)
  result_neg = summarize_list(neg_list)
  
  return len(pos_list), len(neg_list), result_pos, result_neg

