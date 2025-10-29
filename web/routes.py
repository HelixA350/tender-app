from flask import request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
from flask import Blueprint
from tender_agent.utils.state import AgentState, technical_queries, TechnicalFields

bp = Blueprint('routes', __name__)


ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Получаем данные из формы
        analysis_type = request.form.get('analysis_type')
        files = request.files.getlist('files')

        if not analysis_type:
            return render_template('error.html', error_message='Выберите тип анализа')

        if not files or all(f.filename == '' for f in files):
            return render_template('error.html', error_message='Загрузите хотя бы один файл')

        # Директория для загрузки файлов
        uploads_dir = r'web/tmp' #os.environ.get('UPLOAD_FOLDER')
        
        # Проверяем существование директории
        if not uploads_dir or not os.path.exists(uploads_dir):
            return render_template('error.html', error_message='Директория для загрузки не существует')
        
        # Очищаем директорию перед сохранением новых файлов
        try:
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    return render_template('error.html', error_message='Ошибка при удалении прошлых файлов')
        except Exception as e:
            return render_template('error.html', error_message='Ошибка при очистке директории')
        
        # Сохраняем все файлы
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(uploads_dir, filename)
                    file.save(file_path)
                except Exception as e:
                    return render_template('error.html', error_message=f'Ошибка при сохранении файла {file.filename}')
            else:
                return render_template('error.html', error_message='Недопустимый формат файла')

        init_state = AgentState(
            inp_file_dir=uploads_dir,
            queries = technical_queries,
            answer_schema=TechnicalFields
        )

        return redirect(request.url)

    return render_template('submit.html')