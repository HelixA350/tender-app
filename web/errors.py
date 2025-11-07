from flask import request, render_template, jsonify, Blueprint, url_for, redirect
from tender_agent.utils.errors import *
from web import views
from web.models import *
from web.services.file_service import SaveFileError, CreateDirError, InvalidFileFormatError
from web.services.data_service import InvalidAnalysisTypeError, DBError
from web.views import *
from flask_login import login_required, current_user

error_bp = Blueprint('errors', __name__)

# - Ошибки -
class NoAnalysisTypeError(Exception):
    pass
class NoFilesError(Exception):
    pass
class MissingFeedbackFieldsError(Exception):
    pass
class NoNameError(Exception):
    pass
class NoPasswordError(Exception):
    pass
class NoUserError(Exception):
    pass
class NoReportError(Exception):
    pass

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

# --- Обработчики ошибок ---
@error_bp.app_errorhandler(Exception)
def handle_error(e):
    print(e)
    for exc_type, msg in ERROR_MESSAGES.items():
        if isinstance(e, exc_type):
            return render_template('error.html', error_message=msg)
    return render_template('error.html', error_message='Произошла непредвиденная ошибка')