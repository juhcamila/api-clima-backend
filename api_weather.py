import requests, logging

api_weather_key = '76be2322d10ba8d5ccf5533cba6acce7'

def result_clima(body, tipo_api):
    if tipo_api == "api_long":
        result = definir_api_long(body, tipo_api)
        return result
    else:
        result = definir_api_cidade(body, tipo_api)
        return result
       
def definir_api_cidade(body, tipo_api):
    api = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&lang=pt_br&appid={}'.format(body["cidade"], api_weather_key))
    request = api.json()
    result = validations(request, tipo_api)
    return result

def definir_api_long(body, tipo_api):
    api = requests.get("http://api.openweathermap.org/data/2.5/find?lat={}&lon={}&lang=pt_br&cnt=1&appid={}".format(body["lat"], body["long"], api_weather_key))
    request = api.json()
    result = validations(request, tipo_api)
    return result
    
def validations(request, tipo_api):
    if int(request["cod"]) != 200:
        return {"result": request["cod"], "message": "Cidade informada não foi encontrada"}
    else: 
        return create_json(request, tipo_api)

def create_json(request, tipo_api):
    if tipo_api == "api":
        temp_min = kelvin_to_celsius(request["main"]["temp_min"])
        temp_max = kelvin_to_celsius(request["main"]["temp_max"])
        cidade = request["name"]
        clima = request["weather"][0]["description"]
        img_url = definir_img_url(clima)

        return  {"temp_min": temp_min, "temp_max": temp_max, "cidade": cidade, "clima": clima, img_url: img_url}
    else:
        request = request["list"][0]
        temp_min = kelvin_to_celsius(request["main"]["temp_min"])
        temp_max = kelvin_to_celsius(request["main"]["temp_max"])
        cidade = request["name"]
        clima = request["weather"][0]["description"]
        img_url = definir_img_url(clima)

        return  {"temp_min": temp_min, "temp_max": temp_max, "cidade": cidade, "clima": clima, img_url: img_url}

def kelvin_to_celsius(kelvin):
    result = float(kelvin) - 273.15
    return int(result)

def definir_img_url(clima):
    if clima == "ensolarado":  
        return "https://cdn.acritica.net/img/pc/450/300/dn_noticia/2019/06/1560516670.jpg"
    elif clima == "nublado":
        return "https://img.freepik.com/fotos-gratis/streetlights-no-dia-nublado_23-2148098648.jpg?size=626&ext=jpg"
    elif clima == "chuva leve":
        return "https://www.se.gov.br/uploads/image/image/250624/mobile_c8cf0a3d0d019989469947a4ad82b177.jpg"  
    elif clima == "trovoada":
        return "https://www.explicatorium.com/images/fisica/relampagos-e-trovoes.jpg"
    else: 
        return "https://s2.glbimg.com/PE9lTOWcKUlnHVGSjv_OqVcPM7w=/e.glbimg.com/og/ed/f/original/2019/10/25/cloud-blue-high-clouds-its-in-the-air-sky-air-2294671.jpg"    


