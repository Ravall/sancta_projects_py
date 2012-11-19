tests:
	python sancta/manage.py test --settings=settings.test
cs:
	pep8 sancta

integrate: cs tests