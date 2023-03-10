from flask import Flask, render_template, jsonify, request
from webrisk_cmd import do_lookup, do_update, do_evaluate, do_submission, do_extendedcoverage
import myconfig
import random
import os

basedir = os.path.abspath(os.path.dirname(__file__))

key = myconfig.WEBRISK_API_KEY
project_id = myconfig.PROJECT_ID

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


@app.route('/')
def index_view():
    return render_template("index.html")


@app.route('/lookup', methods=['POST'])
def lookup_view():
    # print(request.json)
    url = request.json.get('url')
    print(url)
    url = url.replace(":", "%3A").replace("/", "%2F")
    print(url)
    result = do_lookup(url)
    if result is not None:
        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Somthing went wrong. Please try again later.'}), 400


@app.route('/update', methods=['POST'])
def update_view():
    result = do_update()
    if result is not None:
        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Somthing went wrong. Please try again later.'}), 400


@app.route('/submission', methods=['POST'])
def submission_view():
    url = request.json.get('url')
    print(url)
    result = do_submission(project_id, url)
    if result is not None:
        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Somthing went wrong. Please try again later.'}), 400


@app.route('/evaluate', methods=['POST'])
def evaluate_view():
    url = request.json.get('url')
    print(url)
    result = do_evaluate(url)
    if result is not None:
        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Somthing went wrong. Please try again later.'}), 400


@app.route('/ext-coverage', methods=['POST'])
def ext_coverage_view():
    url = request.json.get('url')
    print(url)
    url = url.replace(":", "%3A").replace("/", "%2F")
    url = '&uri=' + url
    print(url)
    result = do_extendedcoverage(url)
    if result is not None:
        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Somthing went wrong. Please try again later.'}), 400


@app.route('/random-url', methods=['POST'])
def random_url():
    try:
        with open(os.path.join(basedir, 'random_urls.txt')) as file:
            urls = [line.rstrip() for line in file]
        if len(urls) > 0:
            selected_url = random.choice(urls)
            print(selected_url)
            return jsonify({'result': selected_url})
    except IOError as e:
        print(e)
    return jsonify({'error': 'Somthing went wrong. Please try again later.'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
