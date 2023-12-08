from flask_mail import Mail


mail = Mail()

def config_email(app):
    # Configurar Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'grupo19proyectosoftwareunlp@hotmail.com'
    app.config['MAIL_PASSWORD'] = 'grupo19123'

    mail.init_app(app)
