# Database Setup

This project uses PostgreSQL to store the curriculum and learner progress.

## Local Development Setup

### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database

```bash
# Login as postgres user
sudo -u postgres psql

# In psql:
CREATE DATABASE sprachassistent;
CREATE USER youruser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE sprachassistent TO youruser;
\q
```

### 3. Configure Environment

Update your `.env` file with the database URL:
```
DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/sprachassistent
```

### 4. Initialize and Seed Database

```bash
cd backend
python seed_db.py
```

This will:
- Create all necessary tables (units, learner_progress)
- Seed the database with A1.1 curriculum units

## Database Models

### Unit
Stores curriculum units for each CEFR level.

Fields:
- `id` (str, PK): Unique identifier (e.g., "a1_1_u1")
- `level` (str): CEFR level (e.g., "A1.1", "A1.2")
- `title` (str): Unit title
- `objectives` (JSON): List of learning objectives
- `target_vocab` (JSON): List of target vocabulary words

### LearnerProgress
Tracks individual learner progress through the curriculum.

Fields:
- `id` (int, PK): Auto-increment ID
- `learner_id` (str): Learner identifier (for multi-user support)
- `level` (str): Current CEFR level
- `completed_unit_ids` (JSON): List of completed unit IDs
- `mistakes_log` (JSON): List of mistakes for review
- `current_unit_id` (str): Currently active unit
- `created_at` (datetime): Record creation timestamp
- `updated_at` (datetime): Last update timestamp

## Adding New Curriculum Levels

1. Add new units to `app/curriculum/units.py`
2. Update the seed script `seed_db.py` to include the new level
3. Run `python seed_db.py` to seed the new units

## Production Deployment

For production, use a managed PostgreSQL service:
- **Heroku**: Heroku Postgres
- **AWS**: RDS PostgreSQL
- **DigitalOcean**: Managed PostgreSQL
- **Render**: PostgreSQL

Update `DATABASE_URL` in your production environment variables.
