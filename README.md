# publications

Static site for showing publications

For now, don't include bibfile.

Uses custom version of apa.csl (citation style file), so we can reorder the
fields (title first, not name first).

## Building locally

- Install Jekyll's [requirements](https://jekyllrb.com/docs/installation/)
- From the root directory, run `gem install jekyll bundler`, which will install
  jekyll and the other required packages.
- Run `bundle install` to install all the missing gems listed in the `Gemfile`.
- From the root directory, run `bundle exec jekyll serve --livereload`, then
  open `localhost:4000` in your browser

## Questions

- how separate conference articles and abstracts? both are `inproceedings`
    - additional TYPE key in aux file
    - currently, that shows up in the reference string, so maybe use a different key?
- where does abstract text come from?
- issue with last name Martin: https://github.com/inukshuk/bibtex-ruby/issues/169
    - if necessary, can work around this by cycling through with javascript after but boy that's hacky
    - actually: have prepare_bib insert `_-_` into names to prevent the parsing as dates, then have a shell script use sudo to remove that after the build
- multiple people with same last name, e.g., Wang
- what is the COPY key in aux?
- OMIT in aux?
- send me php code to see logic for creation of abstract page?
- link to e.g., Liam's website on abstract page?
    - same with journal link
- have prepare_bib raise informative errors on some validation?
