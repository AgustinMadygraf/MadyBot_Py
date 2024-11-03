"""
Path: src/model/table_creator.py

"""

from sqlalchemy import text
import sqlalchemy
from sqlalchemy.orm import Session
from src.logs.config_logger import LoggerConfigurator
from src.model.table_creation_strategy import TableCreationStrategy

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class TableCreator(TableCreationStrategy):
    """Clase para manejar la creación de tablas en la base de datos."""
    def create_tables(self, session: Session):
        """Crea las tablas necesarias en la base de datos."""
        try:
            # Crear tabla 'usuarios'
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255),
                    email VARCHAR(255),
                    phone_number VARCHAR(20),
                    first_connection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            # Crear tabla 'mensajes'
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    message_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
                )
            """))
            session.commit()
            logger.info("Tablas verificadas/creadas exitosamente.")
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.OperationalError) as e:
            session.rollback()
            logger.error("Error al crear las tablas: %s", e)
