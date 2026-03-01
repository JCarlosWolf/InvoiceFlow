from __future__ import with_statement
import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# -----------------------------------------------------
# Load environment variables (.env)
# -----------------------------------------------------

load_dotenv()

# -----------------------------------------------------
# Add project root to sys.path
# -----------------------------------------------------

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# -----------------------------------------------------
# Import Base and models
# -----------------------------------------------------

from app.database import Base, DATABASE_URL
import app.models  # IMPORTANT: registers models in metadata

# -----------------------------------------------------
# Alembic config
# -----------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# -----------------------------------------------------
# Offline migrations
# -----------------------------------------------------

def run_migrations_offline():
    """Run migrations in 'offline' mode."""

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# -----------------------------------------------------
# Online migrations
# -----------------------------------------------------

def run_migrations_online():
    """Run migrations in 'online' mode."""

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# -----------------------------------------------------
# Entry point
# -----------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()