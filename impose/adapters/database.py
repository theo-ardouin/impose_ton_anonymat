import logging
from sqlite3 import connect, Connection
from contextlib import contextmanager
from collections.abc import Iterator

from impose.adapters.gateway import TaskGateway, ImageGateway, PermissionGateway
from impose.interfaces.database import IDatabase, ISession
from impose.interfaces.gateway import IImageGateway, ITaskGateway, IPermissionGateway

LOGGER = logging.getLogger(__name__)


class Session(ISession):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self._tasks = TaskGateway(self.connection)
        self._images = ImageGateway(self.connection)
        self._perms = PermissionGateway(self.connection)

    @property
    def tasks(self) -> ITaskGateway:
        return self._tasks

    @property
    def images(self) -> IImageGateway:
        return self._images

    @property
    def permissions(self) -> IPermissionGateway:
        return self._perms


class Database(IDatabase):
    FILENAME = "database.db"

    @contextmanager
    def create_session(self) -> Iterator[ISession]:
        try:
            connection = connect(Database.FILENAME)
            self._write_tables(connection)
            yield Session(connection)
            connection.commit()
        except:
            LOGGER.exception("Could not write into database")
            connection.rollback()
        finally:
            connection.close()

    def _write_tables(self, connection: Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
	            channel_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            time TEXT,
                cursor TEXT
            );
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
	            image TEXT NOT NULL UNIQUE
            );
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS permissions (
                user_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
	            scopes TEXT
            );
            """
        )
