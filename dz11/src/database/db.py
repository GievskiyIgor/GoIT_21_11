import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker,create_async_engine
from src.conf.config import config


class DatabaseSessionManager:
    def __init__(self, url:str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        # self.session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False, bind=self._engine)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        
    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not created")
        
        session = self._session_maker()
        
        try:
            yield session
            
        except Exception as err:
            print(err)
            
            await session.rollback()
            
        finally:
            await session.close()
            

sessonmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    async with sessonmanager.session() as session:
        yield session