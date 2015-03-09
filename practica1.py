#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import string

class Acortador(webapp.webApp):

    def parse(self, request):
    
        try:
            metodo = request.split()[0]
            recurso = request.split()[1]
            if metodo == "POST":
                cuerpo = request.split("\r\n\r\n")[1]
            else:
                cuerpo = ""
        except IndexError:
            return None
        return (metodo, recurso, cuerpo)

    def process(self, parsedRequest):

        try:
            metodo, recurso, cuerpo = parsedRequest
        except TypeError:
            return ("400 Bad Request", "<html><body>Solicitud errónea" +
                                       "</html></body>")

        if metodo == "GET" and recurso == "/":
            entrada = "<p><b> Servidor acortador de URLs</b></p>"
            formulario =  '<FORM action="http://localhost:1234"' + \
                          ' method="POST" accept-charset="UTF-8">' + \
                          'URL: <input type="text" name="url">' + \
                          '<input type="submit" value="Acortar"></p></form>'
            lista = "<p>Lista de URLs acortadas:</p>"
            for url in dicc_largo:
                lista = lista + "<p>" + url + "--->" + dicc_largo[url] + "</p>"
                
            htmlResp = "<html><body>" + entrada + formulario + lista + \
                       "</html></body>"
            httpCode = "200 OK"

        elif metodo == "POST" and recurso == "/":
            if len(dicc_largo) == 0:
                self.contador = 0
                        
            if len(cuerpo.split("="))!=2 or cuerpo.split("=")[0]!="url":
                return ("400 Bad Request", "<html><body>Error en el " +
                                           "formulario</html></body>")
            
            url = cuerpo.split("=")[1]
            if url.split("://")[0] != "http" or url.split("://")[0] != "https":
                url = "http://" + url
            
            try:
                url_corta = dicc_largo[url]
            except KeyError:
                url_corta = "http://localhost:1234/" + str(self.contador)
                dicc_largo[url] = url_corta
                dicc_corto[url_corta] = url
            
            htmlResp = "<html><body><p><a href='" + url+ "'>URL</a></p>" + \
                       "<p><a href='" + url_corta + "'>URL Acortada</a></p>" + \
                       "</html></body>"
            httpCode = "200 OK"
            
            self.contador = self.contador + 1
            
        elif metodo == "GET":
            url_corta = "http://localhost:1234" + recurso
            try:
                url = dicc_corto[url_corta]
                print url
            except KeyError:
                return("404 Not Found", "<html><body><p>Recurso no disponible" +
                                        "</p></html></body>")
            htmlResp = '<html><body><head>Redirigiendo... <meta ' + \
                       'http-equiv="refresh" content="1; url=' + url + '" />'
            httpCode = "301 Moved Permanently"
            
        else:
            httpCode = "404 Not Found"
            htmlResp = "<html><body>Método erróneo</body></html>"
            
        return (httpCode, htmlResp)

if __name__ == "__main__":
    dicc_largo = {} #clave URL real
    dicc_corto = {} #clave URL acortada
    AppAcortadora = Acortador("localhost", 1234)
