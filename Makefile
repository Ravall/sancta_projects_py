tests:
	python sancta/manage.py test --settings=settings.test
cs:
	pep8 sancta
	pylint sancta

integrate: cs tests
