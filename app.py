import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html",
                           tasks=mongo.db.tasks.find())


@app.route('/get_categories')
def get_categories():
    return render_template("categories.html",
                           categories=mongo.db.categories.find())

@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/add_category')
def new_category():
    return render_template('add_category.html')

@app.route('/insert_category', methods=['POST'])
def insert_category():
    mongo.db.categories.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)


@app.route('/edit_categorie/<category_id>')
def edit_categorie(category_id):
    the_categorie = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editcategories.html',categorieToedit=the_categorie, categories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks=mongo.db.tasks
    tasks.update( {'_id':ObjectId(task_id)},
    {
        'task_name':request.form.get['task_name'],
        'category_name':request.form.get['category_name'],
        'task_description':request.form.get['task_description'],
        'due_date':request.form.get['due_date'],
        'is_urgent':request.form.get['is_urgent']
    })
    return redirect(url_for('get_tasks'))


@app.route('/update_category/<category_id>', methods=["POST"])
def update_category(category_id):   # need to be equal to {url_for('update_category'
    mongo.db.categories.update(
        {'_id':ObjectId(category_id)},
        {'category_name': request.form.get('category_name')} #request.form.get['category_name'] is bad
    )
    return redirect(url_for('get_categories'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return  redirect(url_for('get_tasks'))


@app.route('/delete_categorie/<category_id>')
def delete_categorie(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))

if __name__== "__main__":
    app.run(host=os.environ.get("IP"), port= int(os.environ.get("PORT", 5000)),debug=True)