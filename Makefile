.PHONY: check test next

check:
	python -m vibe_coding_infra check

test:
	python -m unittest discover -s tests

next:
	python -m vibe_coding_infra next
