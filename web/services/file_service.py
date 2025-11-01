from typing import List
import uuid
import os

# --- Кастомные ошибки ---
class CreateDirError(Exception):
    pass

class InvalidFileFormatError(Exception):
    pass

class SaveFileError(Exception):
    pass

class FileService:
    def __init__(self, dir_path : str):
        """
        Сервис для сохранения файлов
        Args:
            dir_path: str
            Путь к директории куда будут сохраняться файлы
        """
        self.dir_path = dir_path
        self.allowed_extensions = {'pdf', 'docx', 'txt'}

    def save_file(self, files : List[str]):
        """
        Сохраняет все файлы в уникальную директорию внутри {self.dir_path}
        Args:
            files: str
            Список файлов
        Output:
            dir: str
            Путь к директории с сохраненными файлами
        """
        id = self.__create_unique_id()
        dir = self.__create_dir(id)
        for file in files:
            self.__save_single_file(dir, file)
        return dir

    def __create_unique_id(self):
        """Создает уникальный id для папки сохранения"""
        return str(uuid.uuid1())
    
    def __create_dir(self, id : str):
        """Создает директорию для сохранения файлов с названием {id}"""
        try:
            file_dir = os.path.join(self.dir_path, id)
            os.mkdir(file_dir)
            return file_dir
        except:
            raise CreateDirError(f"Не удалось создать директорию {file_dir}")
        
    def __allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

        
    def __save_single_file(self, dir : str, file):
        """Сохраняет один файл в директорию"""
        if file and self.__allowed_file(file.filename):
            try:
                filename = file.filename
                file_path = os.path.join(dir, filename)
                file.save(file_path)
            except Exception as e:
                raise SaveFileError(f"Не удалось сохранить файл {filename}")
        else:
            raise InvalidFileFormatError(f"Недопустимый формат файла {file.filename}")
    
        