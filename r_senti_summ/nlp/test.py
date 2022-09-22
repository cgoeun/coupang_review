import pandas as pd
import numpy as np
import review
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
      r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
  options = Options()
  options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
  # 헤드리스 크롬 도전에 실패했다. 쿠팡에서 막힘.
  # 디버거랑 병행도 안 되는 듯.
  driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  rand_value = random.randint(1, 5)
  
  rv_df = pd.DataFrame(columns=['star','date','review','help'])
  driver.get(str(url))
  driver.implicitly_wait(4)
  time.sleep(1+rand_value/10)
  show_me_reviews = '#btfTab > ul.tab-titles > li:nth-child(2)'
  try:
    driver.find_element(By.CSS_SELECTOR, show_me_reviews).click() 
  except: # 중고 상품 페이지의 경우 상품평 요소가 없다.
    pass
  time.sleep(1+rand_value/10)
  
  cnt = 0
  i = 2
  k = 0
  go = True
  while go:
      pageBtns = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{i}]'
      if i == 13: # page 1 : button[2] ... page 10 : button[11], nxtPage : button[12] -> load page 1
          i = 3 # 2페이지 클릭 유도
          pageBtns = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{i}]'
      try:
          driver.find_element(By.XPATH, pageBtns).click()
      except : 
          go = False
      html = driver.page_source
      soup = BeautifulSoup(html, 'html.parser')
      data = soup.select(".sdp-review__article__list")
      i += 1
      for inx, one in enumerate(data):
          if len(one) > 8: # 리뷰 content가 없는 경우 one의 길이가 7이었다.
              time.sleep(rand_value/10)
              rv = review.Review()   
              print(f'data 있음 {inx}')
              rv.star = int(one.select_one('.sdp-review__article__list__info__product-info__star-orange')['data-rating'])
              rv.date = one.select_one('.sdp-review__article__list__info__product-info__reg-date').get_text()
              try: rv.review = one.select('.sdp-review__article__list__headline')[0].text.strip() + ' '
              except: pass
              try: rv.review += one.select_one('.sdp-review__article__list__review').get_text().strip().replace('\n', ' ')
              except: pass
              try: rv.help = int(one.select_one('.js_reviewArticleHelpfulCount').get_text())
              except: pass
              cnt = 0
              rv_df.loc[k] = [rv.star, rv.date, rv.store, rv.review, rv.help]
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
 
##############################################################################################
max_len = 200
model1 = tf.keras.models.load_model('./nlp/model1/okt_best_model.h5')
okt = Okt()
with open('./nlp/model1/tokenizer.pickle', 'rb') as handle:
    tokenizer1 = pickle.load(handle)
# tokenizer1 = Tokenizer(31400, oov_token = 'OOV') #tf.keras.preprocessing.text.Tokenizer()
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

def tokenize(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
    print(new_sentence)
    new_sentence = okt.morphs(new_sentence)
    print(new_sentence)
    new_sentence = [word for word in new_sentence if not word in stopwords]
    print(new_sentence)
    encoded = tokenizer1.texts_to_sequences([new_sentence])
    print(encoded)
    pad_new = tf.keras.preprocessing.sequence.pad_sequences(encoded, maxlen = max_len)
    print(pad_new)
    return pad_new

def positive_or_negative(url):
  rv_df = get_reviews(url)
  pos_df = pd.DataFrame(columns=['star','date','review','help'])
  neg_df = pd.DataFrame(columns=['star','date','review','help'])
  for idx, t in enumerate(rv_df['review']):
    try:
      score = float(model1.predict(tokenize(t)))
      print(idx, score)
      if score > 0.5 :
        pos_df = pos_df.append(rv_df.iloc[idx,:])
      else : 
        neg_df = neg_df.append(rv_df.iloc[idx,:])
    except : pass
      
  return pos_df, neg_df
# def positive_or_negative(url):
#   rv_df= get_reviews(url)

#   rv_df['label'] = np.nan
#   rv_df['tokenized'] = rv_df['review']
#   for idx, t in enumerate(rv_df['tokenized']):
#     score = float(model1.predict(tokenize(t)))

#     if(score > 0.5):
#       rv_df['label'].iloc[idx] = 1
#     else:
#       rv_df['label'].iloc[idx] = 0
  
#     # if rv_df['star'].iloc[idx]==5:
#     #   rv_df['label'].iloc[idx] = 1
#     # elif rv_df['star'].iloc[idx]== 1 or rv_df['star'].iloc[idx]==2 :
#     #   rv_df['label'].iloc[idx] = 0
 
#     pos_df = rv_df[rv_df['label']==1]
#     neg_df = rv_df[rv_df['label']==0]
 
#     return pos_df, neg_df
############################################################################################################################
tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")
# tokenizer = PreTrainedTokenizerFast.from_pretrained('./nlp/pretrained_model')
# model = BartForConditionalGeneration.from_pretrained('./nlp/pretrained_model')

# def summarize_series(series):
#   summarized = []
#   for sents in series:
#     sents = sents['review'].tolist()
#     summarized.append(summarize_list(sents))
#   return summarized
  
def summarize_list(list):
  sents = ' '.join(list)
  input_ids = tokenizer.encode(sents, return_tensors="pt")

  summary_text_ids = model.generate(
      input_ids=input_ids,
      bos_token_id=model.config.bos_token_id,
      eos_token_id=model.config.eos_token_id,
      length_penalty=2.0,
      max_length=40,
      min_length=20,
      num_beams=4,
  )
  return tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
   
 
def summarize(url):
  # first_start_time = time.time()
  pos_df, neg_df = positive_or_negative(url)

  p_sample = pos_df['review'].sample(frac=0.2, random_state=42)
  n_sample = neg_df['review'].sample(frac=1, random_state=42)
  
  pos_list = p_sample.tolist()
  neg_list = n_sample.tolist()
  # pos_list = []
  # for i in range(len(p_sample)):
  #   pos_list.append(p_sample.iloc[i*10:i*10+10,:])
  
  # neg_list = []
  # for j in range(len(n_sample)//10):
  #   neg_list.append(n_sample.iloc[j*10:j*10+10,:])
    
  result_pos = summarize_list(pos_list)
  result_neg = summarize_list(neg_list)
  
  return len(p_sample), len(n_sample), result_pos, result_neg

print(summarize('https://www.coupang.com/vp/products/4971807634'))