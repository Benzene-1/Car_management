from flask import Blueprint
from flask import render_template, request
from flask import redirect
from flask import url_for
admin = Blueprint('admin', __name__, template_folder='templates/admin')
