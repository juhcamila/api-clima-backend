import requests

from flask import Flask, jsonify, request

from flask_caching import Cache

from api_weather import result_clima

app = Flask(__name__)
# For more configuration options, check out the documentation
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# defina a configuração do cache (isso pode ser feito em um arquivo de settings)
app.config['CACHE_TYPE'] = 'simple'

# instancie o cache e atribua a sua aplicação
app.cache = Cache(app)   

@app.route('/', methods=['POST'])
@app.cache.cached(timeout=60 * 15)
def cached_view():
    body = request.get_json()
    if("long" not in body):
       requests = result_clima(body, "api")
    else:
       requests = result_clima(body, "api_long")      
    
    return requests

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')