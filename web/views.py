from web import file_service, agent_service, data_service
import os
from web.models import User
from flask import redirect, url_for
from flask_login import login_user

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

class Views:
    def __init__(self):
        pass

    def handle_form_submission(self, request, user):
        """Обработка отправки формы
        Args:
            request: Запрос
        Returns:
            response: Ответ
            id: ID записи об анализе в БД
        """
        # Получаем данные из формы
        analysis_type = request.form.get('analysis_type')
        files = request.files.getlist('files')

        # Проверяем правильность заполнения формы
        if not analysis_type:
            raise NoAnalysisTypeError('Не выбран тип анализа')
        if not files or all(f.filename == '' for f in files):
            raise NoFilesError('Не выбраны файлы')
        
        # Вызываем сервисы
        file_dir = file_service.save_file(files)
        result = agent_service.call_agent(file_dir, analysis_type)
        response = result['result']
        id = data_service.record_data(
            analysis_type=analysis_type,
            file_paths=[os.path.join(file_dir, file.filename) for file in files],
            response=response,
            user=user
        )
        return response, id
    
    def handle_feedback_submit(self, request):
        data = request.get_json()
        overall = data.get('overall')
        message = data.get('message')
        analysis_id = data.get('analysis_id')
        if not overall or not message or not analysis_id:
            raise MissingFeedbackFieldsError('Не заполнены обязательные поля')
        else:
            data_service.record_feedback(analysis_id, overall, message)
        return None
    
    def handle_login(self, request):
        name = request.form.get('name')
        password = request.form.get('password')

        # Проверяем правильность заполнения формы
        if not name:
            raise NoNameError('Нет имени')
        if not password:
            raise NoPasswordError('Нет пароля')
        
        user = User.query.filter_by(name=name).first()
        if user and user.check_password(password):
            login_user(user)
        else:
            raise NoUserError('Неверное имя или пароль')


    def get_report(self, id):
        if id:
            return data_service.get_report(id)
        else:
            raise NoReportError('Нет отчета с таким ID')
        
    def handle_index(self, user):
        return data_service.get_user_requests(user)