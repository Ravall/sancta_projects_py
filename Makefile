PYLINT=	pylint
PYLINT_OPTIONS=-iy -rn -d 'R0801,R0904,R0903,C0111,W0142,W0141,F0401,W0108,W0232,W0105,I' \
	--generated-members=filter,id,relation_name

tests:
	python sancta/manage.py test --settings=config.test


integrate: pylint-strict-real tests

NEXT_RELEASE=$(shell perl -pe 's/^(\d+)\.(\d+)\.(\d+)$$/qq{$$1.}.($$2+1).".0"/e' release)
next_release:
	echo $(NEXT_RELEASE)
	git checkout develop
	git pull origin develop
	git flow release start $(NEXT_RELEASE)
	echo $(NEXT_RELEASE) > release
	git add release
	git commit -m "Bumped release version to $(NEXT_RELEASE)"

NEXT_HOTFIX=$(shell perl -pe 's/^(\d+)\.(\d+)\.(\d+)$$/qq{$$1.$$2.}.($$3+1)/e' release)
hotfix:
	echo $(NEXT_HOTFIX)
	git checkout master
	git flow hotfix start $(NEXT_HOTFIX)
	echo $(NEXT_HOTFIX) > release
	git add release
	git commit -m "Bumped release version to $(NEXT_HOTFIX)"


# Приложения, которые полностью проходят проверки pep8/pylint
STRICT_STYLE_FILES=\
	sancta/api \
	sancta/config \
	sancta/hell
# Преобразуем список файлов в список модулей - для pylint
STRICT_STYLE_MODULES=$(shell echo $(STRICT_STYLE_FILES) | perl -pe 's|/|.|g; s/\.py//g')

pylint-strict-real:
	$(PYLINT) -f parseable --ignore=migrations $(PYLINT_OPTIONS) $(STRICT_STYLE_MODULES)