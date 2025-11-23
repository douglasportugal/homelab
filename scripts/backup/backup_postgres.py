import os
import subprocess
import datetime
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASES = os.getenv("DATABASE", "").split(',')
BACKUP_DIR = os.getenv("BACKUP_DIR")
LOG_FILE = os.path.join(BACKUP_DIR, "backup_banco.log")
RETENTION = int(os.getenv("RETENTION", 7))

os.makedirs(BACKUP_DIR, exist_ok=True)

log_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1_000_000,
    backupCount=7
)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def backup_database(db_name):
    date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{db_name}_{date}.sql.gz"
    filepath = os.path.join(BACKUP_DIR, filename)

    os.makedirs(BACKUP_DIR, exist_ok=True)

    try:
        with open(filepath, 'wb') as f:
            process = subprocess.Popen(
                ['pg_dump', '--no-owner', '-h', DB_HOST, '-p', DB_PORT, '-U', DB_USER, db_name],
                stdout=subprocess.PIPE,
                env={**os.environ, 'PGPASSWORD': DB_PASSWORD}
            )
            gzip_process = subprocess.Popen(['gzip'], stdin=process.stdout, stdout=f)
            process.stdout.close()
            gzip_process.communicate()

        if process.wait() != 0:
            raise Exception(f"pg_dump falhou com código {process.returncode}")
        
        logging.info(f"Backup do banco '{db_name}' concluído com sucesso: {filepath}")
        return filepath

    except Exception as e:
        logging.error(f"Erro ao fazer backup do banco '{db_name}': {e}")
        raise

def extrair_data(arquivo):
    try:
        nome = arquivo.rsplit('.', 2)[0]  # remove .sql.gz
        partes = nome.split('_')
        if len(partes) >= 2:
            return datetime.datetime.strptime(partes[-2] + '_' + partes[-1], "%Y%m%d_%H%M%S")
    except Exception:
        pass
    return datetime.datetime.min  # arquivos com nome fora do padrão vão para o fim

def limpar_backups_antigos(db_name, ignorar_arquivo=None):
    arquivos = [
        f for f in os.listdir(BACKUP_DIR)
        if f.startswith(db_name) and f.endswith(".sql.gz")
    ]

    arquivos_ordenados = sorted(arquivos, key=extrair_data, reverse=True)
    antigos = [f for f in arquivos_ordenados[RETENTION:] if f != ignorar_arquivo]

    for arq in antigos:
        try:
            os.remove(os.path.join(BACKUP_DIR, arq))
            logging.info(f"Backup antigo removido: {arq}")
        except Exception as e:
            logging.error(f"Erro ao remover backup antigo {arq}: {e}")

def main():
    for db in DATABASES:
        db = db.strip()
        if not db:
            continue
        try:
            backup_path = backup_database(db)
            limpar_backups_antigos(db, os.path.basename(backup_path))
        except Exception:
            pass

if __name__ == "__main__":
    main()
