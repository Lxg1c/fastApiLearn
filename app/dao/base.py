from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        """
            Универсальный метод, который добавляет данные в таблицу
        """
        async with async_session_maker() as session: #Создаем асинхронную сессию
            async with session.begin(): # # Начинаем транзакцию
                new_instance = cls.model(**values) # Создаем новый экземпляр модели с переданными значениями
                session.add(new_instance) # Добавляем новый экземпляр в сессию
                try:
                    await session.commit() # Пытаемся зафиксировать изменения в базе данных
                except SQLAlchemyError as e: # В случае ошибки откатываем транзакцию и пробрасываем исключение дальше
                    await session.rollback()
                    raise e
                return new_instance # Возвращаем созданный экземпляр