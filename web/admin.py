from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from web.models import Analysis, File, AnalysisResult, Feedback
from flask_admin.theme import Bootstrap4Theme
from markupsafe import Markup

def truncate_with_expand(text, max_length=100):
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    short = text[:max_length].rsplit(' ', 1)[0]  # обрезаем по последнему пробелу
    return Markup(
        f'<span class="truncated-text">{short}… '
        f'<a href="#" onclick="this.parentElement.querySelector(\'.full-text\').style.display=\'inline\'; this.style.display=\'none\'; return false;">(развернуть)</a>'
        f'<span class="full-text" style="display:none;">{text[max_length:]}</span>'
        f'</span>'
    )

class MainView(ModelView):
    column_list =['id', 'Файлы', 'Тип анализа', 'Результат', 'Обратная связь (оценка)', 'Обратная свзяь (сообщение)']
    column_select_related_list = [Analysis.files, Analysis.feedback, Analysis.result]
    can_export = True
    column_formatters = {
        'Файлы': lambda v, c, m, p: ', '.join(f.file_name for f in m.files) if m.files else '',
        'Тип анализа': lambda v, c, m, p: m.analysis_type if m else '',
        'Результат': lambda v, c, m, p: truncate_with_expand(m.result.final_response) if m.result else '',
        'Обратная связь (оценка)': lambda v, c, m, p: m.feedback.overall if m.feedback else '',
        'Обратная связь (сообщение)': lambda v, c, m, p: m.feedback.message if m.feedback else '',
    }
    can_delete = False
    can_create = False
    can_edit = False
    can_set_page_size = True
    column_searchable_list = ['files.file_name', 'analysis_type', 'result.final_response', 'feedback.overall', 'feedback.message']

def init_admin(app, db):
    admin = Admin(
        app, 
        name='Админ Панель', 
        url='/admin',
        theme=Bootstrap4Theme(),
    )
    admin.add_view(MainView(Analysis, db.session, 'Все данные'))
    admin.add_views(
        ModelView(File, db.session, 'Файлы'),
        ModelView(AnalysisResult, db.session, 'Результаты'),
        ModelView(Feedback, db.session, 'Отзывы')
    )

    return admin
