import tarfile, os
from dotenv import load_dotenv

load_dotenv()
dbFile = os.getenv('dbFile', None)
if dbFile is None:
    print('Не указан файл базы ...')
    exit()


if not os.path.exists(dbFile):
    print(f'Отсутствует файл базы "{dbFile}"')
    exit()


tarf = dbFile + '.tar.gz'

with tarfile.open(tarf, 'w:gz') as tf:
    tf.add(dbFile)
os.chmod(tarf, 0o600)
print(f'создан архив базы паролей "{tarf}" с размером {os.path.getsize(tarf):,} Б')


