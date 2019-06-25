import datetime
from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, login_required,
                        current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)

app.secret_key = 'nsknfN,.EIO83739)#Nnkje!(**)048)^ryH'

# set up the login manager for the app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect to the login view

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    # g is a global object that gets passed around
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connectino after each request."""
    g.db.close()
    return response


###################################
# VIEWS
###################################

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<username>')
@app.route('/<username>/')
@login_required
def user_page(username):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        try:
            user = models.User.select().where(
                        models.User.username**username).get()
            try:
                applications = user.get_applications()
            except models.DoesNotExist:
                abort(404)
            events = user.get_events()
            contacts = user.get_contacts()
            return render_template('userpage.html', user=user,
                applications=applications, events=events, contacts=contacts)
        except models.DoesNotExist:
            abort(404)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay! You've been registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            date_joined=datetime.datetime.now()
        )
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/<username>/application/new_application', methods=['GET', 'POST'])
@login_required
def new_application(username):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        form = forms.NewApplicationForm()
        if form.validate_on_submit():
            flash("Yay! You've created a new application to track!", "success")
            models.Application.create(
                date_applied=form.date_applied.data,
                company_name=form.company_name.data,
                job_title=form.job_title.data,
                notes=form.notes.data,
                phone_interview=form.phone_interview.data,
                in_person_interview=form.in_person_interview.data,
                application_contact=form.application_contact.data,
                user=g.user.id
            )
            return redirect(url_for('user_page', username=username))
    return render_template('new_application.html', form=form)


@app.route('/<username>/application/<int:application_id>/edit_application', methods=['GET', 'POST'])
@login_required
def edit_application(username, application_id):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        application = models.Application.get(models.Application.id**application_id)
        form = forms.EditApplicationForm(obj=application)
        if form.validate_on_submit():
            flash("Application edited!", "success")
            application.date_applied = form.date_applied.data
            application.company_name = form.company_name.data
            application.job_title = form.job_title.data
            application.notes = form.notes.data
            application.phone_interview = form.phone_interview.data
            application.in_person_interview = form.in_person_interview.data
            application.application_contact = form.application_contact.data
            application.save()
            return redirect(url_for('user_page', username=username))
        return render_template('edit_application.html', form=form)


@app.route('/<username>/application/<int:application_id>/delete', methods=['GET', 'POST'])
def delete_application(username, application_id):
    """Delete an entry"""
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        application = models.Application.get(models.Application.id**application_id)
        application.delete_instance()
        flash("Application successfully deleted.")
        return redirect(url_for('user_page', username=username))


@app.route('/<username>/event/new_event', methods=['GET', 'POST'])
@login_required
def new_event(username):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        form = forms.NewEventForm()
        if form.validate_on_submit():
            flash("Yay! You've created a new event to track!", "success")
            models.Event.create(
                event_date=form.event_date.data,
                event_name=form.event_name.data,
                event_type=form.event_type.data,
                event_location=form.event_location.data,
                event_time=form.event_time.data,
                event_cost=form.event_cost.data,
                event_notes=form.event_notes.data,
                user=g.user.id
            )
            return redirect(url_for('user_page', username=username))
    return render_template('new_event.html', form=form)


@app.route('/<username>/event/<int:event_id>/edit_event', methods=['GET', 'POST'])
@login_required
def edit_event(username, event_id):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        event = models.Event.get(models.Event.id**event_id)
        form = forms.EditEventForm(obj=event)
        if form.validate_on_submit():
            flash("Event edited!", "success")
            event.event_date=form.event_date.data
            event.event_name=form.event_name.data
            event.event_type=form.event_type.data
            event.event_location=form.event_location.data
            event.event_time=form.event_time.data
            event.event_cost=form.event_cost.data
            event.event_notes=form.event_notes.data
            event.save()
            return redirect(url_for('user_page', username=username))
        return render_template('edit_event.html', form=form)

@app.route('/<username>/event/<int:event_id>/delete', methods=['GET', 'POST'])
def delete_event(username, event_id):
    """Delete an entry"""
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        event = models.Event.get(models.Event.id**event_id)
        event.delete_instance()
        flash("Event successfully deleted.")
        return redirect(url_for('user_page', username=username))




########################################################################

@app.route('/<username>/contact/new_contact', methods=['GET', 'POST'])
@login_required
def new_contact(username):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        form = forms.NewContactForm()
        if form.validate_on_submit():
            flash("Yay! You've created a new contact to track!", "success")
            models.Contact.create(
                contact_name=form.contact_name.data,
                contact_current_company=form.contact_current_company.data,
                contact_title=form.contact_title.data,
                contact_phone=form.contact_phone.data,
                contact_email=form.contact_email.data,
                contact_is_reference=form.contact_is_reference.data,
                contact_notes=form.contact_notes.data,
                user=g.user.id
            )
            return redirect(url_for('user_page', username=username))
    return render_template('new_contact.html', form=form)


@app.route('/<username>/contact/<int:contact_id>/edit_contact', methods=['GET', 'POST'])
@login_required
def edit_contact(username, contact_id):
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        contact = models.Contact.get(models.contact.id**contact_id)
        form = forms.EditContactForm(obj=contact)
        if form.validate_on_submit():
            flash("contact edited!", "success")
            contact.contact_name=form.contact_name.data
            contact.contact_current_company=form.contact_current_company.data
            contact.contact_title=form.contact_title.data
            contact.contact_phone=form.contact_phone.data
            contact.contact_email=form.contact_email.data
            contact.contact_is_reference=form.contact_is_reference.data
            contact.contact_notes=form.contact_notes.data
            contact.save()
            return redirect(url_for('user_page', username=username))
        return render_template('edit_contact.html', form=form)

@app.route('/<username>/contact/<int:contact_id>/delete', methods=['GET', 'POST'])
def delete_contact(username, contact_id):
    """Delete an entry"""
    if username and username != current_user.username:
        return redirect(url_for('index'))
    else:
        contact = models.Contact.get(models.contact.id**contact_id)
        contact.delete_instance()
        flash("Contact successfully deleted.")
        return redirect(url_for('user_page', username=username))







@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('user_page', username=user.username))
            else:
                flash("Your username or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username="ihkeith",
            email="ian.keith@outlook.com",
            password='password',
            date_joined=datetime.datetime.now()
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)