from flask import render_template, jsonify

def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe"
    }
    
    return render_template('error.html', **kwargs), 404

def unauthorized(e):
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": "Debe iniciar sesion para acceder al recurso"
    }
    return render_template('error.html', **kwargs), 401

def badRequest(e):
    error_response = {
            "error": e
        }
    return jsonify(error_response), 400

def parametrosInvalidos():
    return badRequest("Parametros invalidos")