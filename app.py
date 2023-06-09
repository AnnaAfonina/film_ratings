from typing import Tuple, List

from flask import Flask, render_template, request, redirect, url_for
from flask import g

from Film import Film
from films_repository import get_films_to_compare, save_comparison, get_rating

app = Flask(__name__)


# Close handler
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def vs():
    films: Tuple[Film, Film] = get_films_to_compare()
    return render_template('vs.html', films=films)


@app.route('/rating')
def rating():
    films: List[Film] = get_rating()
    return render_template('rating.html', enumerated_films=enumerate(films, start=1))


@app.route('/comparisons', methods=['POST'])
def add_comparison():
    win_id = int(request.form.get('win'))
    lose_id = int(request.form.get('lose'))
    save_comparison(win_id, lose_id)
    return redirect(url_for('vs'))


if __name__ == '__main__':
    app.run()
