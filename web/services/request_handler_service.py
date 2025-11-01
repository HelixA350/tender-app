from web import file_service, agent_service, data_service
import os

# - Ошибки -
class NoAnalysisTypeError(Exception):
    pass

class NoFilesError(Exception):
    pass

class HandlerService:
    def __init__(self):
        pass

    def handle_form_submission(self, request):
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
        )
        return response, id