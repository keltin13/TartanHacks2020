from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app.forms import *
from app.models import User
from random import randint
import sys
from app.database.scrape import *
from app.database.main import *
from app.database.leaderboard import *

# Home Page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# User System Pages
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Get the user from the database
        user = User.query_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Then login the user
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html', title="Signed Out")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        id = randint(0,999999)
        user = User(id, form.username.data, form.password.data)
        #user.set_password(form.password.data)
        update_users({'user_id':id, 'username':form.username.data, 'total':10, 'password_hash':form.password.data},
                        'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    # Get the user from the database
    user = User.query_username(username)
    bets = User.query_user_bets(user.id)
    return render_template('user.html', user=user, bets=bets)

# Betting Divisions
@app.route('/ncaab', methods=['GET', 'POST'])
def ncaab():
    #form = PlaceBetForm()
    live_bets = User.query_league_bets('NCAA')
    forms = []
    i = 0
    for key in live_bets:
        bet = live_bets[key]
        #print(bet)
        forms.append(PlaceBetForm())
        forms[-1].team.choices = [('left', bet['team-1']), ('right', bet['team-2'])]
        forms[-1].bet_id.label = key
        forms[-1].team1.label = bet['team-1']
        forms[-1].team2.label = bet['team-2']
        forms[-1].line1.label = bet['line1']
        forms[-1].line2.label = bet['line2']
        forms[-1].odds1.label = bet['odds1']
        forms[-1].odds2.label = bet['odds2']

    for form in forms:
        if form.validate_on_submit() and form.bet_id.label == form.index.data:
            flash('Bet placed!')
            if form.team.data == 'left':
                team = live_bets[form.index.data]['team-1']
            else:
                team = live_bets[form.index.data]['team-2']
            print(team)
            new_user_bets({'user_id':current_user.id, 'bet_id':form.bet_id.label, 'team':team, 'value':form.bet.data},
                            'C://Users/kelti/Documents/GitHub/TartanHacks2020/website/app/database/data.json')
            return redirect(url_for('ncaab'))

    return render_template('ncaab.html', title='SafeBet - NCAAB', forms=forms, live_bets=live_bets)

@app.route('/leaderboard')
def leaderboard():
    leaderboard = calc_leaderboard()
    return render_template('leaderboard.html', title='Leaderboard', leaderboard=leaderboard)
