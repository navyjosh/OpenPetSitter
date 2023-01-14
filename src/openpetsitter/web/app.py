from flask import Flask, render_template, url_for, flash, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from datetime import date
from openpetsitter.config import CONFIG as cfg
from openpetsitter.data_model.users import User
from openpetsitter.data_model.pets import Pet
from openpetsitter.data_model.jobs import Job
from openpetsitter.web.forms import LoginForm, PetForm, DeletePetForm, AddNewJobForm
from flask_login import current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import select



app = Flask(__name__)
login_manager=LoginManager()

@app.route('/')
def home():
    return render_template('index.html.j2')

@app.route('/pets')
@login_required
def my_pets():
    with cfg.session() as db:
        pets = db.query(Pet).where(Pet.owner == current_user).all()
    return render_template('pets.html.j2', pets=pets)

@login_manager.user_loader
def load_user(user_id):
    with cfg.session() as db:
        return db.query(User)\
            .filter(User.id == int(user_id)).one_or_none()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with cfg.session() as db:
            user = db.query(User).filter(User.username==form.data['username']).one_or_none()            
            login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')            

        return redirect(next or url_for('home'))
    return render_template('login.html.j2', form=form)

@app.route("/add-pet", methods=['GET', 'POST'])
@login_required
def add_pet():
    form = PetForm(owner=current_user)
    if form.validate_on_submit():
        with cfg.session() as db:
            pet = Pet(
                name=form.data['name'],
                dob=form.data['dob'],
                pettype=form.data['pettype'],
                owner=current_user
            )
            db.add(pet)
            db.commit()
        flash('Successfully added a new pet!')
        return redirect(url_for('my_pets'))
    return render_template('add-pet.html.j2', form=form)


@app.route("/add-job/", methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddNewJobForm(owner=current_user)
    
    with cfg.session() as db:            
        pets = db.query(Pet.id).where(Pet.owner_id == current_user.id).all()
        form.pets.choices = pets
    if request.method=='GET':        
            return render_template('add-job.html.j2', form=form)
        
    if form.validate_on_submit():
        print('test')
        with cfg.session() as db:
            job = Job(
                title=form.title.data,
                description=form.description.data,
                pets=form.pets.data,
                date=form.date.data,
                time=form.time.data
            )
            db.add(job)
            db.commit()

        flash('Successfully added new job!')
        return redirect(url_for('my_jobs'))    
    


@app.route("/edit-pet/<int:pet_id>", methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    form = PetForm(owner=current_user)    
    if request.method=='POST':        
        if form.validate_on_submit():            
            with cfg.session() as db:
                pet = db.get(Pet, pet_id)
                pet.name = form.name.data
                pet.dob = form.data['dob']
                pet.pettype = form.data['pettype'] 
                print(pet.name)                           
                db.commit()
            flash('Successfully updated your pet!')
            return redirect(url_for('my_pets'))
    if request.method=='GET':
        with cfg.session() as db:
            p = db.get(Pet, pet_id)
            if p.owner == current_user:
                form = PetForm()
                form.name.data = p.name
                form.dob.data = p.dob
                form.pettype.data = p.pettype
    
    return render_template('edit-pet.html.j2', pet=p, form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/delete-pet/<int:pet_id>", methods=['GET', 'POST'])
@login_required
def delete_pet(pet_id):
    form = DeletePetForm()
    if form.validate_on_submit():
        with cfg.session() as db:
            p = db.get(Pet, pet_id)
            if p.owner_id == current_user.id:
                db.delete(p)
                db.commit()
        flash ('Successfully deleted pet!')
        return redirect(url_for('my_pets'))

    with cfg.session() as db:
        p = db.get(Pet, pet_id)
        if p is not None:
            if p.owner == current_user:
                return render_template('delete-pet.html.j2', pet=p, form=DeletePetForm())
    
    return None

@app.route("/jobs/")
@login_required
def my_jobs():
    with cfg.session() as db:
        # jobs = db.query(Job).where(Job.owner == current_user).options().all()
        jobs = db.scalars(
            select(Job)\
                .options(joinedload(Job.pets))\
                .options(joinedload(Job.sitter))\
                .where(Job.owner == current_user)                
        ).all()
    return render_template('jobs.html.j2', jobs=jobs)




@app.route("/delete-job/<int:job_id>", methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    # form = DeletePetForm()
    # if form.validate_on_submit():
    #     with cfg.session() as db:
    #         p = db.get(Pet, pet_id)
    #         db.delete(p)
    #         db.commit()
    #     flash ('Successfully deleted pet!')
    #     return redirect(url_for('my_pets'))

    # with cfg.session() as db:
    #     p = db.get(Pet, pet_id)
    #     if p is not None:
    #         if p.owner == current_user:
    #             return render_template('delete-pet.html.j2', pet=p, form=DeletePetForm())
    # return None
    return render_template('jobs.html.j2')



if __name__=='__main__':    
    login_manager.login_view = 'login'
    login_manager.init_app(app)    
    app.config['SECRET_KEY'] = cfg.csrf_secret
    with cfg.session() as db:        
        if db.query(User).where(User.username=='josh').one_or_none() is None:            
            u = User(username='josh', usertype='owner')
            u.set_password('test')
            db.add(u)
            pet = Pet(
                name='Rose',
                dob=date(2014,3,6), 
                pettype='dog',
                owner=u
            )
            db.add(pet)
            pet = Pet(
                name='Winston',
            dob=date(2020,4,15),
                pettype='dog',
                owner=u
            )            
            db.add(pet)
            db.commit()
    app.run(debug=True)
