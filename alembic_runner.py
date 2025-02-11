import os
from pathlib import Path
from alembic.config import Config
from alembic import command
from theflow.settings import settings

def run_alembic():
    try:
        # Get the directory containing alembic.ini
        this_dir = Path(__file__).parent
        alembic_ini_path = this_dir / "libs" / "ktem" / "alembic.ini"
        
        # Create Alembic config
        alembic_cfg = Config(str(alembic_ini_path))
        
        # Set the SQLAlchemy URL from your settings
        alembic_cfg.set_main_option("sqlalchemy.url", settings.KH_DATABASE)
        
        # Set the script location
        migrations_dir = this_dir / "libs" / "ktem" / "migrations"
        alembic_cfg.set_main_option("script_location", str(migrations_dir))
        
        print("Generating initial migration for creating tables...")
        # Generate the initial migration
        command.revision(alembic_cfg, autogenerate=True, message="Initial migration")
        
        print("Creating database tables and applying migrations...")
        # This will create tables and run all migrations
        command.upgrade(alembic_cfg, "head")
        
        print("Database tables created and migrations completed successfully!")
        
    except Exception as e:
        print(f"Error during database migration: {str(e)}")
        raise

if __name__ == "__main__":
    run_alembic()

