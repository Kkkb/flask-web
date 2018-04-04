from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Length(1, 64),
											 Email()])
	username = StringField('用户名', validators=[
		Required(), Length(1, 64)])
	password = PasswordField('密码', validators =[
		Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已被注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已被使用')


class LoginForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Length(1, 64), 
											 Email()])
	password = PasswordField('密码', validators=[Required()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('旧密码', validators=[DataRequired()])
	password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('确认新密码', validators=[DataRequired()])
	submit = SubmitField('确定')


class PasswordResetRequestForm(FlaskForm):
	email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
	password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('重设密码')

class ChangeEmailForm(FlaskForm):
	email = StringField('新邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('密码', validators=[DataRequired()])
	submit = SubmitField('确定')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已被注册')