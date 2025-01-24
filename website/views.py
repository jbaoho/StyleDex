# different pages that user can navigate to besides the login page
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Item
from . import db
import json


views = Blueprint('views', __name__)

# define a decorater and declare a function under it
# essentially defining a page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user=current_user)

@views.route('/closet')
@login_required
def closet():
    return render_template("closet.html", user=current_user)

@views.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        clothing_type = request.form.get('clothing_type')
        brand = request.form.get('brand')
        size = request.form.get('size')
        color = request.form.get('color')
        material = request.form.get('material')
        description = request.form.get('description')
        new_item = Item(user_id=current_user.id, clothing_type=clothing_type, brand=brand, size=size, color=color, material=material, description=description)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added!', category='success')
        return redirect(url_for('views.closet'))
    return render_template("insert.html", user=current_user)

@views.route('/delete-item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    itemId = item['itemId']
    item = Item.query.get(itemId)
    if item:
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
        
    return jsonify({})