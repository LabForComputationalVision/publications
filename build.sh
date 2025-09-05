#!/usr/bin/env bash

# validate files for non-unicode
grep -axv '.*' bibliography_files/simoncelli.bib && exit 1
grep -axv '.*' bibliography_files/simoncelli.bibaux && exit 1
grep -axv '.*' bibliography_files/*txt && exit 1
grep -axv '.*' bibliography_files/abstracts/*txt && exit 1

python bibliography_files/prepare_bib.py bibliography_files/simoncelli.bib --aux bibliography_files/simoncelli.bibaux --abstracts bibliography_files/abstracts/ --author_url bibliography_files/authorURL.txt --journal_url bibliography_files/journalURL.txt
bundle exec jekyll build -d ./_site/publications
sed -E -i.backup "s/(h2.*)'\{e\}/\1é/g" _site/publications/author.html
sed -E -i.backup "s/(h2.*)\`\{e\}/\1è/g" _site/publications/author.html

# not sure how to get paths working correctly here
bundle exec htmlproofer _site --ignore-urls "/cgi.media.mit.edu/,/sites.stat.columbia.edu/liam/" --checks Links,Scripts,Images > htmlproofer.log 2>&1
