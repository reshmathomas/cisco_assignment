from flask import Flask, request
from malware_url_lookup_service import malware_url_lookup_service

app = Flask(__name__)

@app.route('/v1/urlinfo/', methods=['GET'])
def get():
    url = request.args.get('url')
    try:
        is_url_malware = malware_url_lookup_service(url).validate()
    except:
        print "Error occured during validation of url."
        raise

    if is_url_malware:
        return url + ": Malware!"
    else:
        return url + ": NOT a malware!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
