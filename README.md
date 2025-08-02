# publications

Static site for showing publications

For now, don't include bibfile.

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

- pdf-url field always included? or folder on webserver?
- abstract-url field? looks redundant
- how to handle chain of superseding? if A supersedes B which supersedes C, should C point to A or B? currently, A and B (original website just had B)
- what are POSTER/TALK? they don't seem to be used
- what's going on with the | in the journalURL file?

## Notes

- To find non-unicode characters, run `grep -axv '.*' PATH`. Then remove the offending character in text editor.

## TODO

- [ ] open issues: 
  - [ ] [last name Martin](https://github.com/inukshuk/jekyll-scholar/issues/366) parsed as date
  - [ ] [group names](https://github.com/inukshuk/jekyll-scholar/issues/367) not being rendered correctly
- [ ] both those can be fixed by running sed afterwards if necessary
- [x] author and journal urls
- [x] exclude/filter
    - CONFABSTRACT is an extra type that comes from bibaux, handle that like tech report type
    - POSTER/TALK appear to still not exist
- [x] popup
- [ ] put together build script
- [ ] include htmlproofer as post build step
- [ ] document "extras", in bibaux file and abstract folder
