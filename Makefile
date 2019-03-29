doc:
	cat connection.yml comments.yml relations_*.yml > .tbls.yml
	DEBUG=1 tbls doc --force --er-format svg

diff:
	cat connection.yml comments.yml relations_*.yml > .tbls.yml
	DEBUG=1 tbls diff

lint:
	cat connection.yml lint.yml comments.yml relations_*.yml > .tbls.yml
	tbls lint > lint_result

dupcheck:
	pipenv run dupcheck

completion: column_comments.yml lint_result
	pipenv run completion
