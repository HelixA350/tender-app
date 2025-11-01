from flask import request, render_template, jsonify
from flask import Blueprint
from tender_agent.utils.errors import *
from web import handler
from web.models import *
from web.services.file_service import SaveFileError, CreateDirError, InvalidFileFormatError
from web.services.data_service import InvalidAnalysisTypeError, DBError
from web.services.request_handler_service import *

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
    MissingFeedbackFieldsError: 'Не заполнены обязательные поля обратной связи'
}

# --- Маршруты ---
@bp.get('/')
def index():
    """Главная страница"""
    return render_template('submit.html')

@bp.post('/')
def submit():
    """Обработка формы"""
    try:
    # Обработка запроса
        response, id = handler.handle_form_submission(request)
        return render_template('results.html', analysis_results=response, analysis_id=id)
    
    # Обработка ошибок
    except Exception as e:
        for exc_type, msg in ERROR_MESSAGES.items():
            if isinstance(e, exc_type):
                return render_template('error.html', error_message=msg)
        return render_template('error.html', error_message='Произошла непредвиденная ошибка')

@bp.post('/feedback')
def feedback():
    """Обработка отзыва пользователя"""
    try:
        handler.handle_feedback_submit(request)
        return jsonify({'status': 'ok'}), 200
    
    # Обработка ошибок
    except Exception as e:
        for exc_type, msg in ERROR_MESSAGES.items():
            if isinstance(e, exc_type):
                return render_template('error.html', error_message=msg)
        return render_template('error.html', error_message='Произошла непредвиденная ошибка')
