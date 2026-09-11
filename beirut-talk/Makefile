# Marp slide build. marp-cli is fetched on first use via npx; no global install.
MARP ?= npx -y @marp-team/marp-cli@latest
SRC := talk.md

.PHONY: html pdf watch serve clean

html: talk.html
pdf: talk.pdf

talk.html: $(SRC)
	$(MARP) $(SRC) --allow-local-files -o $@

# PDF export drives an installed Chrome/Chromium/Edge via puppeteer.
talk.pdf: $(SRC)
	$(MARP) $(SRC) --pdf --allow-local-files -o $@

# Rebuild talk.html on every save.
watch:
	$(MARP) -w $(SRC) --allow-local-files -o talk.html

# Local preview server with live reload.
serve:
	$(MARP) -s .

clean:
	rm -f talk.html talk.pdf
