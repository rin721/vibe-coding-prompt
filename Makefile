.PHONY: check test kb next

check:
	python -m vibe_coding_infra check

test:
	python -m unittest discover -s tests

kb:
	python -m vibe_coding_infra knowledge-import

next:
	python -m vibe_coding_infra next
