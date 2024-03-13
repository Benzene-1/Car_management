from flask import Blueprint
from flask import render_template, request
from website import db
from website.models import User


admin = Blueprint('admin', __name__, template_folder='templates/admin')


@admin.route('/user_management', methods=['GET', 'POST'])
def user_management():
    if request.method == 'POST':
        print(request.form)
        user_id = request.form.get('user_id', None)
        print(f"User ID: {user_id}")
        if user_id is not None:
            user = User.query.get(user_id)
            print(f"User: {user}")
            return render_template('user_management.html', user=user)
    else:
        users = User.query.all()
        return render_template('user_management.html', users=users)


@admin.route('/update_user_status/<int:id>', methods=['POST'])
def update_user_status(id):
    print(f"User ID: {id} updating status...")
    print(f"Request args: {request.form}")
    user = User.query.get(id)
    if user:
        # Assuming the name of the select element is 'select'
        new_status = request.form.get('select')
        user.active_status = new_status
        db.session.commit()
        return f"User status updated to {new_status}!"
    else:
        return 'User not found', 404
