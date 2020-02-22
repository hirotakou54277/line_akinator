from collections import defaultdict

from flask import render_template, request, abort
from tanakinator import app, handler
from tanakinator.models import Solution, Question
from tanakinator.akinator import get_feature_table

CIRCLE_CHAR = '&#9675;'
CROSS_CHAR  = '&#10005;'

@app.route('/')
def root():
    feature_table = get_feature_table()
    table = defaultdict(dict)
    solutions = {s.id: s.name    for s in Solution.query.all()}
    questions = {q.id: q.message for q in Question.query.all()}
    for s_id, features in feature_table.items():
        for q_id, value in features.items():
            table[s_id][q_id] = CIRCLE_CHAR if value == 1.0 else CROSS_CHAR
    return render_template('index.html', solutions=solutions, questions=questions, table=table)

@app.route('/solutions/<int:solution_id>/edit')
def solution_edit(solution_id):
    solution = Solution.query.get(solution_id)
    feature_table = {f: Question.query.get(f.question_id) for f in solution.features}
    kwargs = {'solution': solution, 'feature_table': feature_table}
    return render_template('solutions/edit.html', **kwargs)


from linebot.exceptions import InvalidSignatureError

@app.route('/line', methods=['POST'])
def line_webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature.")
        print("Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
