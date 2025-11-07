from web import file_service, agent_service, data_service
import os
from web.models import User
from flask import session
from flask_login import login_user
from web.errors import *

class Views:
    def __init__(self):
        pass

    def handle_form_submission(self, request, user):
        """Обработка отправки формы
        Args:
            request: Запрос
        Returns:
            tuple: Ответ агента, ID записи в БД, история запросов пользователя
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

        # Добавляем запрос в историю запросов пользователя в сессии
        session['user_requests'].append({
            'id': f'{id}',
            'name': os.path.basename(str(files[0].filename))
        })

        history = session.get('user_requests')
        return response, id, history
    
    def handle_feedback_submit(self, request):
        """Обработка формы обратной связи
        Args:
            request: Запрос, Flask request
        """
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
        """Обработка формы авторизации
        Args:
            request: Запрос, Flask request
        """
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


    def handle_report_view(self, id, user):
        """Получение отчета из истории запросов
        Args:
            id: ID записи об анализе в БД
        Returns:
            Значение поля final_response в объекте AnalysisResult, привянном к объекту Analysis
        """
        try:
            history = session.get('user_requests')
            report = data_service.get_report(id)
            print(id)
            return report, history
        except:
            raise NoReportError('Нет отчета с таким ID')
        
    def handle_index_view(self, user):
        """Получение истории запросов пользователя для отрисовки на главной странице
        При выполнении этого запроса обновляется список запросов пользователя в сессии
        Args:
            user: Пользователь
        Returns:
            Список запросов пользователя, объекты Analysis
        """
        analysis = data_service.get_user_requests(user)
        analysis = session['user_requests'] = [{
            'id': str(a.id),
            'name': os.path.basename(str(a.files[0].file_name))
        } for a in analysis]
        return analysis