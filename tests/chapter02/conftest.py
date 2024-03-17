import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.architecture_python.chapter02.database.orm import metadata, start_mappers


# @pytest.fixture(scope="session")
# def in_memory_db():
#     engine = create_engine("sqlite:///:memory:")
#     metadata.create_all(engine)
#     return engine


# @pytest.fixture(scope="session")
# def session(in_memory_db):
#     start_mappers()
#     yield sessionmaker(bind=in_memory_db)()
#     clear_mappers()



@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    session = sessionmaker(bind=in_memory_db)()
    yield session
    clear_mappers()
    # 각 테스트 케이스 실행 후 세션 롤백
    session.rollback()
    session.close()

# @pytest.fixture(autouse=True)
# def clear_data(session):
#     # 각 테스트 실행 후 데이터 클리어
#     for table in reversed(Base.metadata.sorted_tables):
#         session.execute(table.delete())
#     session.commit()