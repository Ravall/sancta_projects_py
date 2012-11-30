tests:
	python sancta/manage.py test --settings=settings.test
cs:
	pylint -iy -rn -d 'R0904,R0903,C0111,W0142,W0141,F0401,W0108,I' sancta
	pep8 sancta

integrate: cs tests
