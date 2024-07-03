from flask import render_template, flash , redirect, url_for, request, jsonify , session, send_file
from flask_login import current_user , login_user , logout_user, login_required
from urllib.parse import urlsplit
import json

from app import app, db , login
from app.forms import LoginForm, SponcerRegistration, InfluncerRegistration, CampainForm, addAdsForm , addAdsFormFind
from app.models import Sponcer, Influencer, Admin , Campaign, Advertisement

from datetime import date

import matplotlib.pyplot as plt
import io
import base64
import pandas as pd



@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]


    campain = Campaign.query.filter(Campaign.spons_index == current_user.id ).all()     
    
    return render_template('index.html', title='Home', posts=posts, campain= campain)


@app.route('/registerinfluncer', methods=['POST', 'GET'])
def registerinfluncer():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = InfluncerRegistration()


    if form.validate_on_submit():
        influencer = Influencer(
            username=form.username.data, 
            name=form.name.data, 
            image = form.image.data,
            industry  = form.industry.data,
            description = form.description.data,
            youtube = form.youtube.data, 
            insta = form.insta.data, 
            facebook = form.facebook.data,
            min_budget = form.min_budget.data,
        
            niche = form.niche.data,
            rating = 0,
            flagged = False,
            )
        influencer.set_password(form.password.data)
        db.session.add(influencer)
        db.session.commit()
        flash('Congratulations, you are now a Influencer! lets Rock :)')
        return redirect(url_for('login'))
    return render_template('register_influncer.html', title='Register', form=form)
 

@app.route('/registersponcer', methods=['POST', 'GET'])
def registersponcer():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SponcerRegistration()


    if form.validate_on_submit():
        sponcer = Sponcer(
            flagged = False,
            username=form.username.data, 
            name=form.name.data, 
            image = form.image.data,
            description = form.description.data,
            industry  = form.industry.data,
            rating = 0, 
        )
        sponcer.set_password(form.password.data)
        db.session.add(sponcer)
        db.session.commit()

        flash('Congratulations, you are now a sponcer! lets Rock :)')
        return redirect(url_for('login'))
    return render_template('register_sponcer.html', title='Register', form=form)





@login.user_loader
def load_user(user_id):
    user_role = session.get('user_role')
    if user_role == 'sponcer':
        return Sponcer.query.get(int(user_id))
    elif user_role == 'influencer':
        return Influencer.query.get(int(user_id))
    elif user_role == 'admin':
        return Admin.query.get(int(user_id))
    return None



@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == 'admin':
            user = Admin.query.filter_by(username=form.username.data).first()
        elif form.role.data == 'influencer':
            user = Influencer.query.filter_by(username=form.username.data).first()
        elif form.role.data == 'sponcer':
            user = Sponcer.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        session['user_role'] = form.role.data  # Store the user role in the session
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for(form.role.data, username=user.username)
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))







############################# Sponcer routes #########################

@app.route('/sponcer/<username>')
@login_required
def sponcer(username):
    user = Sponcer.query.filter_by(username=username).first_or_404()

    campains = Campaign.query.filter(Campaign.spons_index == current_user.id).all()
    influncers = Influencer.query.all()
    return render_template('sponcer_user.html', user=user, campains = campains, influncers = influncers)

@app.route('/sponcer/<username>/find')
@login_required
def sponcerfind(username):
    user = Sponcer.query.filter_by(username=username).first_or_404()

    campains = Campaign.query.filter(Campaign.spons_index == current_user.id).all()
    influncers = Influencer.query.all()
    return render_template('find.html', user=user, campains = campains, influncers = influncers)


@app.route('/sponcer/<username>/campain')
@login_required
def sponcercampain(username):
    user = Sponcer.query.filter_by(username=username).first_or_404()

    campains = Campaign.query.filter(Campaign.spons_index == current_user.id).all()      

    return render_template('campainPage.html', user=user, campains = campains)


@app.route('/sponcer/<username>/campain/add',  methods=['POST', 'GET'])
@login_required
def sponcercampain_add(username):

    form = CampainForm()

    if form.validate_on_submit():
        
        # termJson = json.dumps([{'term':form.goals, 'user': current_user}])  #todo there is some error
        
        campain = Campaign(
        name = form.name.data, 
        image = form.image.data, 
        description = form.description.data,  
        start_date = form.start_date.data, 
        end_date = form.end_date.data, 
        visibility = form.visibility.data, 
        goals = {}, 
        budget = form.budget.data, 
        spons_index = current_user.id
            
            )
        
        db.session.add(campain)
        db.session.commit() 
        flash('New campaign Added')
        return redirect(url_for('sponcercampain', username=username))
    else:
        flash('Campaign is not added Something is wrong')
        
    return render_template('addCampain.html', form= form)




@app.route('/sponcer/<username>/<campainId>')
@login_required
def CampainProfilePage(username,campainId):
    user = Sponcer.query.filter_by(username=username).first()
    campain = Campaign.query.filter_by(id=campainId).first()
    ads = Advertisement.query.filter_by(camp_id = campainId).all()
    

    
    return render_template('CampainProfilePage.html', user=campain, uuuser = user, ads = ads) ######## here there is some fuck up (but working fine no change req) because we are use base profile  



@app.route('/sponcer/<username>/<campainId>/adsAdd' , methods=['POST', 'GET'])
@login_required
def addAds(username,campainId):
    user = Sponcer.query.filter_by(username=username).first()
    campain = Campaign.query.filter_by(id=campainId).first()


    form = addAdsForm()

    if form.validate_on_submit():
        
        # termJson = json.dumps([{'term':form.goals, 'user': current_user}])  #todo there is some error
        termJson = {}  #todo there is some error
        
        ads = Advertisement(
            name = form.name.data ,
            description = form.description.data ,
            term = termJson ,
            payment = form.payment.data ,
            influencer_id = form.influencer_id.data ,                         #todo not actually connected to the influencer
            camp_id = campain.id,
            statusAccepted = 'pi'                                              # pi in pending from influncer
            )
        
        db.session.add(ads)
        db.session.commit()
        flash('New Advertisement  Added')
        return render_template('CampainProfilePage.html', user=campain, uuuser = user)
    else:
        flash('Campaign is not added Something is wrong')
        
    return render_template('addAds.html', form= form)


@app.route('/sponcer/find/<username>/<influncerId>/adsAdd' , methods=['POST', 'GET'])
@login_required
def addAdsFromFind(username,influncerId):
    
    user = Sponcer.query.filter_by(username=username).first()
    # influncer = Influencer.query.filter_by(id=influncerId).first()


    form = addAdsFormFind()

    if form.validate_on_submit():
        
        # termJson = json.dumps([{'term':form.goals, 'user': current_user}])  #todo there is some error
        termJson = {}  #todo there is some error


        campain = Campaign.query.filter_by(id=form.campainId.data).first()
        
        if campain is not None:
            ads = Advertisement(
                name = form.name.data ,
                description = form.description.data ,
                term = termJson ,
                payment = form.payment.data ,
                influencer_id = influncerId,     
                camp_id = form.campainId.data    ,   #todo not actually connected to the influencer
                statusAccepted = 'pi'                                              # pi in pending from influncer
                )

            db.session.add(ads)
            db.session.commit()
            flash('New Advertisement  Added')

            return render_template('CampainProfilePage.html', user=campain, uuuser = user)
        else:
            flash('Campaign not found')
    else:
        flash('Advertisement is not added Something is wrong')
        
    return render_template('addAdsFind.html', form= form)



@app.route('/sponcer/<username>/<campainId>/<adId>')
@login_required
def viewAds(username,campainId,adId):

    ads = Advertisement.query.filter_by(id=adId).first()


    return render_template('adsView.html', ads= ads)






# @app.route('/sponcer/<username>/stats')
# @login_required
# def sponcerstats(username):
#     user = Sponcer.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)



############################# Influencer routes #########################


@app.route('/influencer/<username>')
@login_required
def influencer(username):
    user = Influencer.query.filter_by(username=username).first_or_404()

    # Dummy data for illustration purposes
    campains = Campaign.query.filter(Campaign.spons_index == 1).all()
    influncers = Influencer.query.all()
    return render_template('influncerProfilePage.html', user=user)

@app.route('/influencer/<username>/find')
@login_required
def influencerfind(username):
    user = Influencer.query.filter_by(username=username).first_or_404()

    campains = Campaign.query.filter().all()
    # influncers = Influencer.query.all()
    return render_template('find.html', user=user, campains = campains)

# @app.route('/influencer/<username>/stats')
# @login_required
# def influencerstats(username):
#     user = Sponcer.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)







############################# Admin routes #########################
@app.route('/admin/<username>')
@login_required
def admin(username):
    user = Admin.query.filter_by(username=username).first_or_404()

    # Dummy data for illustration purposes
    campains = Campaign.query.filter(Campaign.spons_index == 1).all()
    Fcampains = Campaign.query.filter(Campaign.spons_index == 1).all()
    Fnfluncers = Influencer.query.filter_by(flagged=True).all()
    return render_template('influncerProfilePage.html', user=user) 

@app.route('/admin/<username>/find')
@login_required
def adminfind(username):
    user = Influencer.query.filter_by(username=username).first_or_404()

    campains = Campaign.query.filter().all()
    # influncers = Influencer.query.all()
    return render_template('find.html', user=user, campains = campains)

# @app.route('/admin/<username>/stats')
# @login_required
# def adminstats(username):
#     user = Sponcer.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)


@app.route('/influencer/editinfluncer', methods=['POST', 'GET'])
@login_required
def editinfluncer():
    
    
    form = InfluncerRegistration()
    if request.method == 'GET':

        form.name.data = current_user.name
        form.username.data = current_user.username
        form.image.data = current_user.image
        form.industry.data = current_user.industry
        form.description.data = current_user.description
        form.youtube.data = current_user.youtube
        form.insta.data = current_user.insta
        form.facebook.data = current_user.facebook
        form.min_budget.data = current_user.min_budget
        form.niche.data = current_user.niche

    if form.validate_on_submit():

        current_user.username=form.username.data
        current_user.name=form.name.data
        current_user.image = form.image.data
        current_user.industry  = form.industry.data
        current_user.description = form.description.data
        current_user.youtube = form.youtube.data 
        current_user.insta = form.insta.data 
        current_user.facebook = form.facebook.data
        current_user.min_budget = form.min_budget.data
        current_user.niche = form.niche.data
        
        flash('Your changes have been saved.')
    
        
        db.session.commit()

        return redirect(url_for('editinfluncer'))
    
    return render_template('register_influncer.html', title='Edit Profile', form=form)

@app.route('/influencer/editsponcer', methods=['POST', 'GET'])
@login_required
def editsponcer():
    
    
    form = SponcerRegistration()
    if request.method == 'GET':

        form.name.data = current_user.name
        form.username.data = current_user.username 
        form.image.data = current_user.image
        form.industry.data = current_user.industry  
        form.description.data = current_user.description
   

    if form.validate_on_submit():

         
        current_user.username=form.username.data
        current_user.name=form.name.data
        current_user.image = form.image.data
        current_user.industry  = form.industry.data
        current_user.description = form.description.data

  
        
        flash('Your changes have been saved.')
    
        
        db.session.commit()

        return redirect(url_for('sponcer', username = current_user.username))
    
    return render_template('register_sponcer.html', title='Edit Profile', form=form)

@app.route('/influencer/editcampain/<campainId>', methods=['POST', 'GET'])
@login_required
def editcamapin(campainId):
    
    campain = Campaign.query.filter_by(id=campainId).first()
    form = CampainForm()
    if request.method == 'GET':

                
        
        form.name.data = campain.name
        form.image.data = campain.image
        form.description.data = campain.description
        form.start_date.data = campain.start_date
        form.end_date.data = campain.end_date
        form.visibility.data = campain.visibility
        form.budget.data = campain.budget
        current_user.id = campain.spons_index

        goals = {}

   

    if form.validate_on_submit():

     
        campain.name = form.name.data
        campain.image = form.image.data
        campain.description = form.description.data
        campain.start_date = form.start_date.data
        campain.end_date = form.end_date.data
        campain.visibility = form.visibility.data
        campain.budget = form.budget.data
        current_user.id = campain.spons_index

    
        flash('Your changes have been saved.')
    
        flash('New campaign Added')
        return redirect(url_for('sponcercampain', username=current_user.username))
    else:
        flash('Campaign is not added Something is wrong')
        
    return render_template('addCampain.html', form= form)

@app.route('/delete_user', methods=['POST', 'GET'])
@login_required
def delete_user():
    user_role = session.get('user_role')
    
    if user_role == 'sponcer':
        user = Sponcer.query.get(current_user.id)
    elif user_role == 'influencer':
        user = Influencer.query.get(current_user.id)
    elif user_role == 'admin':
        user = Admin.query.get(current_user.id)
    else:
        flash('User role not recognized')
        return redirect(url_for('index'))

    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.')
        logout_user()  # Log the user out after deletion
        return redirect(url_for('login'))
    else:
        flash('User not found')
        return redirect(url_for('index'))

@app.route('/confirm_delete_user')
@login_required
def confirm_delete_user():
    return render_template('confirm_delete_user.html')










################################################STATS #################################

@app.route('/sponcer/<username>/stats')
@login_required
def sponcerstats(username):
    user = Sponcer.query.filter_by(username=username).first_or_404()

    # Fetch all campaigns and their budgets
    campaigns = Campaign.query.filter(Campaign.spons_index == user.id).all()
    total_budget = sum(campaign.budget for campaign in campaigns)
    
    # Prepare data for the pie chart
    campaign_names = [campaign.name for campaign in campaigns]
    campaign_budgets = [campaign.budget for campaign in campaigns]
    
    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(campaign_budgets, labels=campaign_names, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Fetch all advertisements
    ads = Advertisement.query.join(Campaign, Advertisement.camp_id == Campaign.id).filter(Campaign.spons_index == user.id).all()

    # Prepare data for influencers and their prices
    influencer_data = []
    for ad in ads:
        influencer = Influencer.query.get(ad.influencer_id)
        influencer_data.append({
            'name': influencer.name,
            'campaign': Campaign.query.get(ad.camp_id).name,
            'price': ad.payment
        })

    # Data for more graphs
    campaign_durations = [(campaign.name, (campaign.end_date - campaign.start_date).days) for campaign in campaigns]
    campaign_df = pd.DataFrame(campaign_durations, columns=['Campaign', 'Duration'])

    # Create bar chart for campaign durations
    fig, ax = plt.subplots()
    campaign_df.plot(kind='bar', x='Campaign', y='Duration', ax=ax)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    duration_plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('sponcer_stats.html', user=user, total_budget=total_budget, plot_url=plot_url, influencer_data=influencer_data, duration_plot_url=duration_plot_url)


@app.route('/influencer/<username>/stats')
@login_required
def influencerstats(username):
    user = Influencer.query.filter_by(username=username).first_or_404()

    # Fetch all advertisements associated with the influencer
    ads = Advertisement.query.filter_by(influencer_id=user.id).all()
    total_income = sum(ad.payment for ad in ads)
    company_share = total_income * 0.2  # Assuming the company takes a 20% share
    influencer_share = total_income - company_share

    # Prepare data for the pie chart
    shares = ['Influencer', 'Company']
    share_values = [influencer_share, company_share]

    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(share_values, labels=shares, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Follower statistics
    platforms = ['YouTube', 'Instagram', 'Facebook']
    followers = [user.youtube, user.insta, user.facebook]

    # Create bar chart for followers
    fig, ax = plt.subplots()
    ax.bar(platforms, followers)
    ax.set_xlabel('Platform')
    ax.set_ylabel('Followers')
    ax.set_title('Followers on Different Platforms')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    follower_plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('influencer_stats.html', user=user, total_income=total_income, plot_url=plot_url, follower_plot_url=follower_plot_url) 




@app.route('/admin/<username>/stats')
@login_required
def adminstats(username):
    user = Admin.query.filter_by(username=username).first_or_404()

    # Fetch all sponsors and influencers
    total_sponsors = Sponcer.query.count()
    total_influencers = Influencer.query.count()

    # Fetch all campaigns and their budgets
    campaigns = Campaign.query.all()
    total_budget = sum(campaign.budget for campaign in campaigns)

    # Prepare data for the spending pie chart
    sponsor_budgets = {}
    for campaign in campaigns:
        sponsor_id = campaign.spons_index
        if sponsor_id in sponsor_budgets:
            sponsor_budgets[sponsor_id] += campaign.budget
        else:
            sponsor_budgets[sponsor_id] = campaign.budget

    sponsor_names = [Sponcer.query.get(sponsor_id).name for sponsor_id in sponsor_budgets.keys()]
    sponsor_budget_values = list(sponsor_budgets.values())

    # Create pie chart for spending
    fig, ax = plt.subplots()
    ax.pie(sponsor_budget_values, labels=sponsor_names, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    spending_plot_url = base64.b64encode(img.getvalue()).decode()

    # Fetch all advertisements for influencer income graph
    ads = Advertisement.query.all()
    influencer_incomes = {}
    for ad in ads:
        influencer_id = ad.influencer_id
        if influencer_id in influencer_incomes:
            influencer_incomes[influencer_id] += ad.payment
        else:
            influencer_incomes[influencer_id] = ad.payment

    influencers = {inf.id: inf for inf in Influencer.query.all()}
    income_data = [(influencers[id].name, income) for id, income in influencer_incomes.items()]
    income_data.sort(key=lambda x: x[1], reverse=True)
    influencer_names, incomes = zip(*income_data)

    # Create bar chart for influencer incomes
    fig, ax = plt.subplots()
    ax.bar(influencer_names, incomes)
    ax.set_xlabel('Influencer')
    ax.set_ylabel('Income')
    ax.set_title('Income of Influencers')
    plt.xticks(rotation=90)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    income_plot_url = base64.b64encode(img.getvalue()).decode()

    # Most popular influencer (based on total followers across all platforms)
    most_popular_influencer = max(influencers.values(), key=lambda inf: inf.youtube + inf.insta + inf.facebook)
    
    # Sponsor with the biggest budget
    biggest_budget_sponsor = max(Sponcer.query.all(), key=lambda sponcer: sum(camp.budget for camp in Campaign.query.filter(Campaign.spons_index == sponcer.id)))
    biggest_budget_total = sum(camp.budget for camp in Campaign.query.filter(Campaign.spons_index == biggest_budget_sponsor.id))

    # Additional pie charts and scatter plots
    fig, ax = plt.subplots()
    ax.pie([most_popular_influencer.youtube, most_popular_influencer.insta, most_popular_influencer.facebook], 
           labels=['YouTube', 'Instagram', 'Facebook'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    follower_distribution_url = base64.b64encode(img.getvalue()).decode()

    sponsor_budgets = [(sponcer.name, sum(camp.budget for camp in Campaign.query.filter(Campaign.spons_index == sponcer.id))) for sponcer in Sponcer.query.all()]
    sponsor_names, budgets = zip(*sponsor_budgets)

    fig, ax = plt.subplots()
    ax.scatter(budgets, range(len(budgets)))
    ax.set_xlabel('Budget')
    ax.set_ylabel('Sponsor')
    ax.set_yticks(range(len(budgets)))
    ax.set_yticklabels(sponsor_names)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    sponsor_budget_scatter_url = base64.b64encode(img.getvalue()).decode()

    return render_template('admin_stats.html', user=user, 
                           total_sponsors=total_sponsors, total_influencers=total_influencers, 
                           spending_plot_url=spending_plot_url, income_plot_url=income_plot_url, 
                           most_popular_influencer=most_popular_influencer, 
                           biggest_budget_sponsor=biggest_budget_sponsor, biggest_budget_total=biggest_budget_total,
                           follower_distribution_url=follower_distribution_url, 
                           sponsor_budget_scatter_url=sponsor_budget_scatter_url)
 
