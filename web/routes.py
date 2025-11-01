from flask import request, render_template
import os
from flask import Blueprint
from tender_agent.utils.errors import *
from web import file_service, data_service, agent_service
from web.models import *
from web.services.file_service import SaveFileError, CreateDirError, InvalidFileFormatError
from web.services.data_service import InvalidAnalysisTypeError, DBError

bp = Blueprint('routes', __name__)

ERROR_MESSAGES = {
    InvalidAnalysisTypeError: 'Неправильный тип анализа: выбранный тип не поддерживается БД',
    DBError: 'Ошибка при работе с базой данных',
    NoDocumentsError: 'Не удалось загрузить ни один фрагмент текста из документов',
    FailedToCreateVectorstoreError: 'Не удалось создать векторное хранилище из загруженных документов',
    LlmError: 'Ошибка при суммаризации документов языковой моделью',
    SaveFileError: 'Ошибка при сохранении файла, попробуйте еще раз',
    CreateDirError: 'Ошибка при создании директории для сохранения файлов, попробуйте еще раз',
    InvalidFileFormatError: 'Неподдерживаемый формат файла',
    Exception: 'Произошла непредвиденная ошибка'
}

def handle_form_submission(request):
    # Получаем данные из формы
    analysis_type = request.form.get('analysis_type')
    files = request.files.getlist('files')

    # Проверяем правильность заполнения формы
    if not analysis_type:
        return render_template('error.html', error_message='Выберите тип анализа')
    if not files or all(f.filename == '' for f in files):
        return render_template('error.html', error_message='Загрузите хотя бы один файл')
    
    # Вызываем сервисы
    file_dir = file_service.save_file(files)
    result = agent_service.call_agent(file_dir, analysis_type)
    response = result['result']
    data_service.record_data(
        analysis_type=analysis_type,
        file_paths=[os.path.join(file_dir, file.filename) for file in files],
        response=response,
    )
    return response

@bp.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            response = handle_form_submission(request)
            return render_template('results.html', analysis_results=response)
        
        # Обработка ошибок
        except Exception as e:
            for exc_type, msg in ERROR_MESSAGES.items():
                if isinstance(e, exc_type):
                    return render_template('error.html', error_message=msg)
            return render_template('error.html', error_message='Произошла непредвиденная ошибка')

    return render_template('submit.html')


    