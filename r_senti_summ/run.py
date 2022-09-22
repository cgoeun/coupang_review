from operator import index
from flask import Flask, request, render_template, jsonify
import nlp
from flask_socketio import SocketIO
from flask_socketio import send, emit
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segdsgdsfgbdfgbd'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def review_analysis():
    if request.method == 'GET':
        return render_template('index.html')
    else : 
        rv_df, time_crawling = nlp.get_reviews(request.form.get('linkInput').strip()) 
        pos_df, neg_df, time_p_or_n = nlp.positive_or_negative(rv_df)
        len_pos, len_neg, result_pos, result_neg, time_summarize = nlp.summarize(pos_df, neg_df)
        return render_template("index.html", rv_df=rv_df, time_crawling=time_crawling,pos_df=pos_df, neg_df=neg_df, time_p_or_n=time_p_or_n,result_pos=result_pos, result_neg=result_neg, time_summarize=time_summarize, len_pos=len_pos, len_neg=len_neg )
        # res = {'url': nlp.summarize(request.form.get('linkInput'))}
        
        # return jsonify(res)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
     
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    
@socketio.on('crawlingAddr')
def handle_crawlingAddr_event(json):
    print('크롤링 주소: ', json['addr'] )
    # 크롤잉 진행
    rv_df = nlp.get_reviews(json['addr'].strip()) 
    print('크롤링 완료')
    rv_df.to_csv('df.csv')
    emit('crawlingClear', "크롤링 완료")#rv_df.to_json() )

@socketio.on('goPNA')
def handle_goPNA_event():
    rv_df = pd.read_csv('df.csv', index_col=0)
    pos_df, neg_df = nlp.positive_or_negative(rv_df)
    pos_df.to_csv('pos_df.csv')
    neg_df.to_csv('neg_df.csv')
    emit('PNAClear', "긍/부정 감성분석 완료")
    
@socketio.on('goSummary')
def handle_goSummary_event():
    pos_df = pd.read_csv('pos_df.csv', index_col=0)
    neg_df = pd.read_csv('neg_df.csv', index_col=0)
 
    len_pos, len_neg, result_pos, result_neg = nlp.summarize(pos_df, neg_df)
    print( len_pos, len_neg, result_pos, result_neg)
    emit('goSummaryClear', {
        "len_pos":len_pos, 
        "len_neg":len_neg, 
        "result_pos":result_pos.strip(), 
        "result_neg":result_neg.strip(),
        "pos_json":pos_df.to_json(),
        "neg_json":neg_df.to_json()
    } )
    
if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
