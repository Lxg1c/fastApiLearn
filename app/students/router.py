from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent
# Импортируем библиотеки и шаблон

# Настраиваем route
router = APIRouter(prefix='/students', tags=['Работа со студентами'])

# Путь: /students/ получаем всех студентов
@router.get("/", summary="Получить всех студентов")
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentDAO.find_all(**request_body.to_dict())

# Роут: /students/id для получения студента по id
@router.get("/{id}", summary="Получить одного студента по id")
async def get_student_by_id(student_id: int) -> SStudent | dict:
    rez = await StudentDAO.find_full_data(student_id)
    if rez is None:
        return {'message': f'Студент с ID {student_id} не найден!'}
    return rez

@router.get("/by_filter", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudent | dict:
    rez = await StudentDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Студент с указанными вами параметрами не найден!'}
    return rez