from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField, SelectField, BooleanField, RadioField, TextAreaField, widgets
from wtforms.validators import DataRequired, URL, Length, Regexp
from wtforms.widgets import HiddenInput
# from wtforms_alchemy import QuerySelectField


class UserForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    lastname = StringField('Apellido', validators=[DataRequired()])
    rol = SelectField('Rol', coerce=int)
    estado = SelectField('Estado', choices=[(0, 'Inactivo'), (1, 'Activo')], validators=[DataRequired()])
    institutions = SelectMultipleField('Instituciones', coerce=int)  # 'coerce' se usa para asegurarse de que los valores sean int
    submit = SubmitField('Guardar Cambios')

def str_to_bool(value):
    if isinstance(value, str):
        return value.lower() in ['true', '1', 'yes']
    return value

class CreateInstitutionForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    info = StringField('Información de la institución', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    web = StringField('Sitio web', validators=[URL(), Length(max=255)])
    keywords = StringField('Palabras claves (separadas por coma)', validators=[DataRequired()])
    phone = StringField('Teléfono', validators=[
    DataRequired(),
    Regexp(r'^\+?1?\d{9,15}$', message="Número de teléfono inválido")
    ])
    contact_info = StringField('Información de contacto', validators=[DataRequired()])
    enabled = SelectField('Activa', choices=[('True', 'Si'), ('False', 'No')], coerce=str_to_bool)
    days = SelectMultipleField('Días de disponibilidad (debe seleccionar uno o mas días)', 
                               choices=[('lunes', 'Lunes'), ('martes', 'Martes'),
                                        ('miercoles', 'Miércoles'), ('jueves', 'Jueves'),
                                        ('viernes', 'Viernes'), ('sabado', 'Sábado'),
                                        ('domingo', 'Domingo')],
                               option_widget=widgets.CheckboxInput(),
                               widget=widgets.ListWidget(prefix_label=False))
    franja = RadioField('Franja horaria (debe seleccionar uno)', choices=[('manana', 'Mañana'), ('tarde', 'Tarde'), ('ambos', 'Mañana y Tarde')])
    submit = SubmitField('Enviar')