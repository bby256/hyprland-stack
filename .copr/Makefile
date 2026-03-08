srpm:
	set -eu; \
	if ! command -v spectool >/dev/null 2>&1 || ! command -v rpmautospec >/dev/null 2>&1; then dnf -y install rpmdevtools rpmautospec >/dev/null; fi; \
	spec_path="$(spec)"; \
	if [ -z "$$spec_path" ]; then spec_path=$$(find . -maxdepth 1 -name '*.spec' | head -n 1); fi; \
	if [ -z "$$spec_path" ]; then echo "No spec file found" >&2; exit 1; fi; \
	workdir="$$(pwd)"; \
	processed_spec=".copr-rpmautospec.$$(basename "$$spec_path")"; \
	rm -f "$$processed_spec"; \
	spectool -g -R --define "_sourcedir $$workdir" "$$spec_path"; \
	rpmautospec process-distgit "$$spec_path" "$$processed_spec"; \
	rpmbuild -bs "$$processed_spec" --define "_sourcedir $$workdir" --define "_srcrpmdir $(outdir)"; \
	rm -f "$$processed_spec"
