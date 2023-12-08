from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def init_app(app):
    db.init_app(app)

def config_db(app):
    """Recibe la app por parametro y cierra la conexion a la base de datos una vez finaliza el request
    """
    @app.teardown_request
    def close_session(exeception=None):
        db.session.close()
        
def reset_db():
    """tira toda la base de datos y la vuelve a crear"""
    print("inicio de barrido de la base de datos")
    db.drop_all()
    print("barrido completado, inicio de creacion de BD")
    db.create_all()
    print("finalizacion de creacion de BD")

