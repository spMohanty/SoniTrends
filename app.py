from flask import Flask, jsonify, request, send_from_directory, render_template
import requests
requests.packages.urllib3.disable_warnings()
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)


@app.route('/get_trends', methods=['GET'])
def get_trends():
    keywords = request.args.get('q')
    print(keywords)
    keywords = keywords.strip().split(";")
    payload = pytrends.build_payload(keywords, cat=0, timeframe='all', geo='', gprop='')
    df = pytrends.interest_over_time()
    dates = df.index.tolist()
    dates = [str(x).split()[0] for x in dates]
    interests = {}
    for _keyword in keywords:
        interests[_keyword] = df[_keyword].tolist()
    return jsonify({"dates":dates, "interests":interests})

if __name__ == '__main__':
    app.run(debug=True)
