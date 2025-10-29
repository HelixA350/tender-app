from flask import request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
from flask import Blueprint

bp = Blueprint('routes', __name__)


ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        analysis_type = request.form.get('analysis_type')
        files = request.files.getlist('files')

        if not analysis_type:
            print('Выберите тип анализа')
            return redirect(request.url)

        if not files or all(f.filename == '' for f in files):
            print('Загрузите хотя бы один файл')
            return redirect(request.url)

        # Директория для загрузки файлов
        uploads_dir = r'web/tmp' #os.environ.get('UPLOAD_FOLDER')
        
        # Проверяем существование директории
        if not uploads_dir or not os.path.exists(uploads_dir):
            print('Директория для загрузки не существует')
            return redirect(request.url)
        
        # Очищаем директорию перед сохранением новых файлов
        try:
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Ошибка при удалении файла {filename}: {str(e)}')
                    return redirect(request.url)
        except Exception as e:
            print(f'Ошибка при очистке директории: {str(e)}')
            return redirect(request.url)
        
        # Сохраняем все файлы
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(uploads_dir, filename)
                    file.save(file_path)
                except Exception as e:
                    print(f'Ошибка при сохранении файла {file.filename}: {str(e)}')
                    return redirect(request.url)
            else:
                print('Недопустимый формат файла')
                return redirect(request.url)
            
        print('все успешно загружено')

        return redirect(request.url)

    return render_template('submit.html')