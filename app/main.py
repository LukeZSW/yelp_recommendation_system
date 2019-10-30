from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from .models import Item
from . import E, indexdir
from .src.search import person_query_search, query_search

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        queries = request.form.get("query")
        item_index_result = None
        number = 12
        if current_user.is_authenticated:
            user_id = int(current_user.get_id())
            if 0 >= user_id and user_id < 6722:
                item_index_result = person_query_search(indexdir, queries, user_id, E, number)
            else:
                item_index_result = query_search(indexdir, queries, number)
        else:
            item_index_result = query_search(indexdir, queries, number)
        if not item_index_result or len(item_index_result) == 0:
            flash('No result.', 'error')
            return render_template('index.html')
        items = []
        for i in item_index_result:
            item = Item.query.filter_by(id=i).first()
            items.append(item)
        return render_template('index.html', items=items)
    else:
        return render_template('index.html')




