#!/usr/bin/env sh

python bibliography_files/prepare_bib.py bibliography_files/simoncelli.bib --aux bibliography_files/simoncelli.bibaux --abstracts bibliography_files/abstracts/ --author_url bibliography_files/authorURL.txt --journal_url bibliography_files/journalURL.txt
bundle exec jekyll build --verbose -d ./_site
sed -E -i 's/(h2.*)Ja-n/\1Jan/g' _site/author.html
sed -E -i 's/(h2.*)Fe-b/\1Feb/g' _site/author.html
sed -E -i 's/(h2.*)Ma-r/\1Mar/g' _site/author.html
sed -E -i 's/(h2.*)Ap-r/\1Apr/g' _site/author.html
sed -E -i 's/(h2.*)Ma-y/\1May/g' _site/author.html
sed -E -i 's/(h2.*)Ju-n/\1Jun/g' _site/author.html
sed -E -i 's/(h2.*)Ju-l/\1Jul/g' _site/author.html
sed -E -i 's/(h2.*)Au-g/\1Aug/g' _site/author.html
sed -E -i 's/(h2.*)Se-p/\1Sep/g' _site/author.html
sed -E -i 's/(h2.*)Oc-t/\1Oct/g' _site/author.html
sed -E -i 's/(h2.*)No-v/\1Nov/g' _site/author.html
sed -E -i 's/(h2.*)De-c/\1Dec/g' _site/author.html
sed -E -i "s/(h2.*)'{e}/\1é/g" _site/author.html

mv _site publications
mkdir _site
mv publications _site/publications
# not sure how to get paths working correctly here
bundle exec htmlproofer ./_site --checks Link,Scripts,Images
