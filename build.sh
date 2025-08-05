#!/usr/bin/env sh

python bibliography_files/prepare_bib.py bibliography_files/simoncelli.bib --aux bibliography_files/simoncelli.bibaux --abstracts bibliography_files/abstracts/ --author_url bibliography_files/authorURL.txt --journal_url bibliography_files/journalURL.txt
bundle exec jekyll build --verbose -d ./_site/publications
sed -E -i "s/(h2.*)Ja-n/\1Jan/g" _site/publications/author.html
sed -E -i "s/(h2.*)Fe-b/\1Feb/g" _site/publications/author.html
sed -E -i "s/(h2.*)Ma-r/\1Mar/g" _site/publications/author.html
sed -E -i "s/(h2.*)Ap-r/\1Apr/g" _site/publications/author.html
sed -E -i "s/(h2.*)Ma-y/\1May/g" _site/publications/author.html
sed -E -i "s/(h2.*)Ju-n/\1Jun/g" _site/publications/author.html
sed -E -i "s/(h2.*)Ju-l/\1Jul/g" _site/publications/author.html
sed -E -i "s/(h2.*)Au-g/\1Aug/g" _site/publications/author.html
sed -E -i "s/(h2.*)Se-p/\1Sep/g" _site/publications/author.html
sed -E -i "s/(h2.*)Oc-t/\1Oct/g" _site/publications/author.html
sed -E -i "s/(h2.*)No-v/\1Nov/g" _site/publications/author.html
sed -E -i "s/(h2.*)De-c/\1Dec/g" _site/publications/author.html
sed -E -i "s/(h2.*)'\{e\}/\1é/g" _site/publications/author.html

# not sure how to get paths working correctly here
bundle exec htmlproofer _site --ignore-urls "/cgi.media.mit.edu/,/sites.stat.columbia.edu/liam/" --checks Links,Scripts,Images --ignore-status-codes 403  > htmlproofer.log 2>&1
bundle exec htmlproofer _site --ignore-urls "/cgi.media.mit.edu/,/sites.stat.columbia.edu/liam/" --checks Links,Scripts,Images --only-status-codes 403 > htmlproofer-403.log 2>&1
