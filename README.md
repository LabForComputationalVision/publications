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
