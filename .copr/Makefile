srpm:
	set -eu; \
	if ! command -v spectool >/dev/null 2>&1 || ! command -v rpmautospec >/dev/null 2>&1; then dnf -y install rpmdevtools rpmautospec >/dev/null; fi; \
	spec_path="$(spec)"; \
	if [ -z "$$spec_path" ]; then spec_path=$$(find . -maxdepth 1 -name '*.spec' | head -n 1); fi; \
	if [ -z "$$spec_path" ]; then echo "No spec file found" >&2; exit 1; fi; \
	workdir="$$(pwd)"; \
	spec_name="$$(basename "$$spec_path")"; \
	processed_dir=".copr-rpmautospec"; \
	processed_spec="$$processed_dir/$$spec_name"; \
	rm -rf "$$processed_dir"; \
	mkdir -p "$$processed_dir"; \
	spectool -g -R --define "_sourcedir $$workdir" "$$spec_path"; \
	rpmautospec process-distgit "$$spec_path" "$$processed_spec"; \
	cp "$$processed_spec" "$(outdir)/$$spec_name"; \
	rpmbuild -bs "$$processed_spec" --define "_sourcedir $$workdir" --define "_srcrpmdir $(outdir)"; \
	rm -rf "$$processed_dir"
