from flask import request, render_template, jsonify, Blueprint, url_for, redirect, session
from tender_agent.utils.errors import *
from web.models import *
from web.views import Views
from flask_login import login_required, current_user

bp = Blueprint('routes', __name__)
views = Views()

# --- Маршруты ---
@bp.get('/')
@login_required
def index():
    """Главная страница"""
    requests = views.handle_index_view(current_user)
    return render_template('submit.html',
                           current_user=current_user,
                           user_requests=requests,
                           active_request_id=None,
                           )

@bp.post('/')
@login_required
def submit():
    """Обработка формы"""
    response, id, history = views.handle_form_submission(request, current_user)
    return render_template('results.html', analysis_results=response, analysis_id=id, user_requests=history)

@bp.post('/feedback')
@login_required
def feedback():
    """Обработка отзыва пользователя"""
    views.handle_feedback_submit(request)
    return jsonify({'status': 'ok'}), 200


@bp.get('/login')
def login_index():
    """Экран авторизации"""
    return render_template('login.html')

@bp.post('/login')
def login():
    """Обработка авторизации пользователя"""
    views.handle_login(request)
    return redirect(url_for('routes.index'))
    
@bp.get('/report/<analysis_id>')
@login_required
def report(analysis_id):
    """Получить отчет по анализу из истории"""
    results, requests = views.handle_report_view(analysis_id, current_user)
    return render_template('results.html', analysis_results=results, analysis_id=analysis_id, user_requests=requests)

    