from flask import request, render_template, jsonify, Blueprint, url_for, redirect
from tender_agent.utils.errors import *
from web import views
from web.models import *
from web.services.file_service import SaveFileError, CreateDirError, InvalidFileFormatError
from web.services.data_service import InvalidAnalysisTypeError, DBError
from web.views import *
from flask_login import login_required, current_user

bp = Blueprint('routes', __name__)

# --- Сообщения об ошибках, возвращаемые пользователю ---
ERROR_MESSAGES = {
    InvalidAnalysisTypeError: 'Неправильный тип анализа: выбранный тип не поддерживается БД',
    DBError: 'Ошибка при работе с базой данных',
    NoDocumentsError: 'Не удалось загрузить ни один фрагмент текста из документов',
    FailedToCreateVectorstoreError: 'Не удалось создать векторное хранилище из загруженных документов',
    LlmError: 'Ошибка при суммаризации документов языковой моделью',
    SaveFileError: 'Ошибка при сохранении файла, попробуйте еще раз',
    CreateDirError: 'Ошибка при создании директории для сохранения файлов, попробуйте еще раз',
    InvalidFileFormatError: 'Неподдерживаемый формат файла',
    Exception: 'Произошла непредвиденная ошибка',
    NoAnalysisTypeError: 'Не выбран тип анализа',
    NoFilesError: 'Не выбраны файлы',
    MissingFeedbackFieldsError: 'Не заполнены обязательные поля обратной связи',
    NoNameError: 'Не указано имя пользователя',
    NoPasswordError: 'Не указан пароль',
    NoUserError: 'Неверный логин или пароль',
    NoReportError: 'Отчет не найден',
}

# --- Маршруты ---
@bp.get('/')
@login_required
def index():
    """Главная страница"""
    return render_template('submit.html')

@bp.post('/')
@login_required
def submit():
    """Обработка формы"""
    try:
    # Обработка запроса
        response, id = views.handle_form_submission(request, current_user)
        return render_template('results.html', analysis_results=response, analysis_id=id)
    
    # Обработка ошибок
    except Exception as e:
        for exc_type, msg in ERROR_MESSAGES.items():
            if isinstance(e, exc_type):
                print(e)
                return render_template('error.html', error_message=msg)
        return render_template('error.html', error_message='Произошла непредвиденная ошибка')

@bp.post('/feedback')
@login_required
def feedback():
    """Обработка отзыва пользователя"""
    try:
        views.handle_feedback_submit(request)
        return jsonify({'status': 'ok'}), 200
    
    # Обработка ошибок
    except Exception as e:
        for exc_type, msg in ERROR_MESSAGES.items():
            if isinstance(e, exc_type):
                return render_template('error.html', error_message=msg)
        return render_template('error.html', error_message='Произошла непредвиденная ошибка')


@bp.get('/login')
def login_index():
    """Экран авторизации"""
    return render_template('login.html')

@bp.post('/login')
def login():
    """Обработка авторизации пользователя"""
    try:
        views.handle_login(request)
        return redirect(url_for('routes.index'))
    
    # Обработка ошибок
    except Exception as e:
        for exc_type, msg in ERROR_MESSAGES.items():
            if isinstance(e, exc_type):
                return render_template('error.html', error_message=msg)
        return render_template('error.html', error_message='Произошла непредвиденная ошибка')
    
@bp.get('/report/<analysis_id>')
@login_required
def report(analysis_id):
    try:
        results = views.get_report(analysis_id)
        return render_template('results.html', analysis_results=results, analysis_id=analysis_id)
    
    # Обработка ошибок
    except Exception as e:
        for exc_type, msg in ERROR_MESSAGES.items():
            if isinstance(e, exc_type):
                print(e)
                return render_template('error.html', error_message=msg)
        return render_template('error.html', error_message='Произошла непредвиденная ошибка')
    