from web.models import *

# - Кастомные ошибки -
class InvalidAnalysisTypeError(Exception):
    pass
class DBError(Exception):
    pass

class DataService:
    """
    Сервис для сохранения данных о результатах работы и обратной связи
    """
    def __init__(self, db):
        """
        Args:
            db: объект базы данных
        """
        self.db = db
        self.analysis_type = {
            'tz': 'technical'
        }

    def record_data(
        self,
        analysis_type: str,
        file_paths: list,
        response: dict
    ):
        """
        Запись данных о результатах работы
        Args:
            analysis_type: тип анализа
            file_paths: пути к файлам
            response: ответ от агента
        Returns:
            id: id записи в БД об анализе
        """
        analysis_type = self.analysis_type.get(analysis_type)
        if not analysis_type:
            raise InvalidAnalysisTypeError('Неверный тип анализа при сохранении данных в БД')
        try:
            analysis_enum = AnalysisType(analysis_type.lower())
        except ValueError:
            raise InvalidAnalysisTypeError('Неверный тип анализа при сохранении данных в БД')
        
        try:
            new_analysis = Analysis(
                analysis_type=analysis_enum,
            )
            self.db.session.add(new_analysis)
            self.db.session.flush()

            for file_path in file_paths:
                if file_path:
                    new_file = File(
                        analysis_id=new_analysis.id,
                        file_name=file_path
                    )
                    self.db.session.add(new_file)
            new_response = AnalysisResult(
                final_response=str(response),
                analysis_id=new_analysis.id
            )
            self.db.session.add(new_response)
            self.db.session.commit()
            return new_analysis.id
        except:
            raise DBError('Ошибка при записи данных в БД')

    def record_feedback(self, analysis_id, overall, message):
        """Запись обратной связи
        Args:
            analysis_id: id анализа
            overall: сообщение с общей оценкой
            message: подробный комментарий
        """
        try:
            new_feedback = Feedback(
                analysis_id=analysis_id,
                overall=overall,
                message=message
            )
            self.db.session.add(new_feedback)
            self.db.session.commit()
        except:
            raise DBError('Ошибка при записи данных в БД')
