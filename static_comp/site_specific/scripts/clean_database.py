import os
import shutil
import subprocess

def main():
	cur_dir = os.getcwd()
	folder_name = 'toldyouso'
	target_dir = ''.join(cur_dir[:cur_dir.index(folder_name)+len(folder_name)])
	print 'Using basepase: %s' % target_dir
	migration_dir = os.path.join(target_dir, 'myapp', 'migrations')
	print 'Searching for migrations folder...'
	if os.path.exists(migration_dir) and os.path.isdir(migration_dir):
		print 'migrations directory found'
		shutil.rmtree(migration_dir)
		print 'migrations directory deleted'
	else:
		print 'no migrations folder found'
	print 'Searching for mydb file...'
	mydb_dir = os.path.join(target_dir, 'mydb')
	if os.path.exists(mydb_dir) and os.path.isfile(mydb_dir):
		print 'mydb file found'
		os.remove(mydb_dir)
		print 'mydb file deleted'
	else:
		print 'mydb file not found'

	print 'Making migrations...'
	os.chdir(target_dir)
	subprocess.call(['python', 'manage.py', 'makemigrations', 'myapp'])
	print 'Applying migrations'
	subprocess.call(['python', 'manage.py', 'migrate'])

	os.chdir(cur_dir)


if __name__ == '__main__':
	main()
