from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


from webshop.models import User


class NewObject(FlaskForm):
    title = StringField("Tárgy megnevezés:", validators=[DataRequired(), Length(min=3, max=20)])
    description = StringField("Tárgy leírása:", validators=[DataRequired(), Length(min=10, max=100)])
    price = IntegerField("Ár:", validators=[DataRequired()])
    submit = SubmitField("Közzétevés")



class NewUser(FlaskForm):
    username = StringField("Név", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("E-mail cím", validators=[DataRequired(), Email(message="A megadott e-mail cím nem megfelelő!")])
    password = PasswordField("Jelszó", validators=[DataRequired()])
    password_confirm = PasswordField("Jelszó újra", validators=[DataRequired(), EqualTo("password", message="A két jelszó nem egyezik meg egymással!")])
    submit = SubmitField("Regisztráció")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(message="A felhasználónév már foglalt!")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(message="Az e-mail cím már foglalt!")



class LoginForm(FlaskForm):
    username = StringField("Név", validators=[DataRequired()])
    password = PasswordField("Jelszó", validators=[DataRequired()])
    remember = BooleanField("Bejelentkezve maradok")
    submit = SubmitField("Bejeletkezés")



class NewOrder(FlaskForm):
    locate = StringField("Posta cím", validators=[DataRequired()])
    mobil_number = IntegerField("Telefonszám", validators=[DataRequired()])
    submit = SubmitField("Megrendelés")
