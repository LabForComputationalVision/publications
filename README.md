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

- multiple people with same last name, e.g., Wang
- OMIT in aux?
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
- [x] put together build script
- [ ] confabstracts have their journal etc rendered wrong
- [ ] include htmlproofer as post build step
  - finish going through this
- [ ] document "extras", in bibaux file and abstract folder
- [ ] write a script to help validate input files?
