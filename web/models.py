from web import db
from enum import Enum


class AnalysisType(Enum):
    technical = 'technical'


class FeedbackMessages(Enum):
    positive = 'positive'
    negative = 'negative'
    neutral = 'neutral'


class Analysis(db.Model):
    __tablename__ = 'analysis'

    id = db.Column(db.Integer, primary_key=True)
    analysis_type = db.Column(db.Enum(AnalysisType), nullable=True)

    # One-to-many: one Analysis can have many Files
    files = db.relationship('File', back_populates='analysis', cascade='all, delete-orphan')

    # One-to-one: one Analysis has one AnalysisResult
    result = db.relationship('AnalysisResult', back_populates='analysis', uselist=False, cascade='all, delete-orphan')

    # One-to-one: one Analysis has one Feedback
    feedback = db.relationship('Feedback', back_populates='analysis', uselist=False, cascade='all, delete-orphan')


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255))
    # TODO: Добавить тип файла, информацию о том что из него прочитал агент

    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    analysis = db.relationship('Analysis', back_populates='files')


class AnalysisResult(db.Model):
    __tablename__ = 'analysis_result'

    id = db.Column(db.Integer, primary_key=True)
    final_response = db.Column(db.String(10000))
    # TODO: Добавить то какие фрагменты были извлечены для ответа

    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    analysis = db.relationship('Analysis', back_populates='result')


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)  # Добавлен первичный ключ
    overall = db.Column(db.Enum(FeedbackMessages))
    message = db.Column(db.String(10000))

    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    analysis = db.relationship('Analysis', back_populates='feedback')