from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, DateField,
                    SelectField, TimeField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def name_exists(FlaskForm, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with that name already exists.")


def email_exists(FlaskForm, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with that email already exists.")


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, "
                        "and underscores only.")),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
        ])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class NewApplicationForm(FlaskForm):
    date_applied = DateField(
        'Date Applied',
        format='%m/%d/%Y',
        validators=[
            DataRequired()
        ])
    company_name = StringField(
        'Company Name',
        validators=[DataRequired()]
    )
    job_title = StringField(
        'Job Title',
        validators=[DataRequired()]
    )
    notes = TextAreaField(
        'Notes'
    )
    phone_interview = SelectField(
        'Phone Interview',
        choices=[('Yes', 'Yes'), ('No', 'No')
    ])
    in_person_interview = SelectField(
        'In Person Interview',
        choices=[('Yes', 'Yes'), ('No', 'No')
    ])
    application_contact = StringField('Application Contact')


class NewEventForm(FlaskForm):
    event_date = DateField(
        'Event Date',
        format='%m/%d/%Y',
        validators=[DataRequired()]
    )
    event_name = StringField('Event Name',validators=[DataRequired()])
    event_type = SelectField(
        'Event Type',
        validators=[DataRequired()],
        choices=[
            ('Meetup', 'Meetup'),
            ('Job Fair', 'Job Fair'),
            ('Conference', 'Conference')
        ])
    event_location = StringField('Event Location', validators=[DataRequired()])
    event_time = TimeField('Event Time', format='%H:%M %p', validators=[DataRequired()])
    event_cost = StringField(
        'Event Cost',
        validators=[
            Regexp(
                r'\$[0-9]+.[0-9]+',
                message=("Put currency in format of $7.00"))]
    )
    event_notes = TextAreaField('Event Notes')


class NewContactForm(FlaskForm):
    contact_name = StringField('Contact Name', validators=[DataRequired()])
    contact_current_company = StringField('Current Company', validators=[DataRequired()])
    contact_title = StringField('Current Title', validators=[DataRequired()])
    contact_phone = StringField('Phone Number')
    contact_email = StringField('Email Address', validators=[Email()])
    contact_is_reference = SelectField('Reference?', choices=[('Yes', 'Yes'), ('No', 'No')])
    contact_notes = TextAreaField('Notes')


class EditApplicationForm(FlaskForm):
    date_applied = DateField(
        'Date Applied',
        format='%m/%d/%Y',
        validators=[
            DataRequired()
        ])
    company_name = StringField(
        'Company Name',
        validators=[DataRequired()]
    )
    job_title = StringField(
        'Job Title',
        validators=[DataRequired()]
    )
    notes = TextAreaField(
        'Notes'
    )
    phone_interview = SelectField(
        'Phone Interview',
        choices=[('Yes', 'Yes'), ('No', 'No')
    ])
    in_person_interview = SelectField(
        'In Person Interview',
        choices=[('Yes', 'Yes'), ('No', 'No')
    ])
    application_contact = StringField('Application Contact')


class EditEventForm(FlaskForm):
    event_date = DateField(
        'Event Date',
        format='%m/%d/%Y',
        validators=[DataRequired()]
    )
    event_name = StringField('Event Name',validators=[DataRequired()])
    event_type = SelectField(
        'Event Type',
        validators=[DataRequired()],
        choices=[
            ('Meetup', 'Meetup'),
            ('Job Fair', 'Job Fair'),
            ('Conference', 'Conference')
        ])
    event_location = StringField('Event Location', validators=[DataRequired()])
    event_time = TimeField('Event Time', validators=[DataRequired()])
    event_cost = StringField('Event Cost',validators=[
            Regexp(
                r'\$[0-9]+.[0-9]+',
                message=("Put currency in format of $7.00"))]
    )
    event_notes = TextAreaField('Event Notes')