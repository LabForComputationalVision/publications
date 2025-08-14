# publications

This repo builds a static site to display publications from the Lab for Computational Vision. It does so with some python preprocessing using [bibtexparser 2.0](https://bibtexparser.readthedocs.io/), then builds the site with [jekyll](https://jekyllrb.com/) using the  [jekyll-scholar](https://github.com/inukshuk/jekyll-scholar) extension.

## Input files

In order to create this website, several files are used, only the first of which is necessary. All of these files are passed to `prepare_bib.py` in `build.sh`, and so the paths can be changed there.

- `bibliography_files/simoncelli.bib`: a standard bibtex file containing the publications to include. All comments will be ignored, but otherwise the entries from this file will be made available on the details page on the site, **exactly as they appear in this file** (i.e., before they are cleaned up by `prepare_bib.py`).
- `bibliography_files/simoncelli.bibaux`: auxiliary file, structured as a bibtex file but containing non-standard fields. All of these will be merged into file used to build the website, but only the following fields are currently used (case-insensitive): `SUPERSEDES`, `RELATED`, `DOWNLOAD`.
    - Each entry can contain multiple of each of these fields.
    - `SUPERSEDES` and `RELATED` are of the structure: `Title text|KEY`, where `Title text` is the (optional) text to display as the title of a link and `KEY` is the key of another entry in the bibtex file.
    - `DOWNLOAD` is of the structure: `Title text|URL`, where `Title text` is the text to display as the title of a link (non-optional) and `URL` is the url of that link.
    - All of these fields can contain html, though any href fields should not contain quotes.
- `bibliography_files/journalURL.txt`, `bibliography_files/authorURL.txt`: text files defining (optional) urls for authors and journals to use on the detail pages:
    - Both files must have a single item per line, and each line must be of the format: `Name = "URL"`, where `Name` is the string to match and the `URL` is the corresponding url to link. Note that `Name` is case insensitive and ignores spaces.
- `bibliography_files/abstracts`: folder containing article abstracts. Each abstract must be in a separate file named `KEY-abstract.txt`, where `KEY` is the corresponding bibtex key. These files can contain html.
    - Note that to link to the details page of an entry, should use `<a href=KEY.html>`
    - href fields should not contain quotes.
    
All urls should be `https`, to make `htmlproofer` happy.

## Building locally

- Install Jekyll's [requirements](https://jekyllrb.com/docs/installation/)
- From the root directory, run `gem install jekyll bundler`, which will install jekyll and the other required packages.
- Run `bundle install` to install all the missing gems listed in the `Gemfile`.
- Create a python environment and install `bibliography_files/requirements.txt` (`pip install -r bibliography_files/requirements.txt`)
- From the root directory, run the included build script: `./build.sh`. This will create the site in `_site/publications`.
- Either:
    - Navigate to `_site` (`cd _site`) and launch a webserver (`python -m http.server 4000`), then open `localhost:4000` in your browser.
    - Copy over the `_site` directory to your webserver.

## Understanding what's happening

The build script does several things:
- Checks input files for non-unicode characters, raising error code 1 if any are found.
- Runs `bibliography_files/prepare_bib.py`, which cleans up the bibtex file, merges it with the bibaux file, adds in additional information (like urls and abstracts) and saves all this to the location where jekyll expects it.
- Calls `jekyll build` to create the static site.
- Calls `sed` to deal with some jekyll-scholar parsing issues (which may eventually get fixed: [1](https://github.com/inukshuk/jekyll-scholar/issues/367), [2](https://github.com/inukshuk/jekyll-scholar/issues/366)).
- Calls [htmlproofer](https://github.com/gjtorikian/html-proofer) to check for broken html, redirecting the output to `htmlproofer.log`.

The structure of the site is largely controlled by a small number of files, which tell jekyll-scholar how to format the references and detail pages: `site/_layouts/bib.html` (how to format the entries on the main bibliography pages), `site/_layouts/details.html` (how to create the details page for each entry),`site/_includes/reference.html` (the rendering that is shared between the two of these). If you wish to make changes here, looking at the reference for the [liquid templating language](https://shopify.github.io/liquid/) used by jekyll will be helpful, though note that not all features (e.g., `renders`) are included in jekyll's variant.

## Questions

- multiple people with same last name, e.g., Wang
- what's going on with the | in the journalURL file?
    - unsure, double check old site
- missing urls:
    - cgi.media.mit.edu: old MIT tech reports
- then some that look like they should be working but aren't, grep htmlproofer log to find
- CONFABSTRACT showing up in reference string

## Notes

- To find non-unicode characters, run `grep -axv '.*' PATH`. Then remove the offending character in text editor.

## TODO

- [ ] open issues: 
  - [ ] [last name Martin](https://github.com/inukshuk/jekyll-scholar/issues/366) parsed as date
  - [ ] [group names](https://github.com/inukshuk/jekyll-scholar/issues/367) not being rendered correctly
- [x] both those can be fixed by running sed afterwards if necessary
- [x] author and journal urls
- [x] exclude/filter
    - CONFABSTRACT is an extra type that comes from bibaux, handle that like tech report type
    - POSTER/TALK appear to still not exist
- [x] popup
- [x] put together build script
- [x] confabstracts have their journal etc rendered wrong
- [x] include htmlproofer as post build step
- [x] fix htmlproofer?
    - [x] tildes getting messed up in urls
    - [x] robbe's page has moved
    - [ ] missing files in cns.nyu.edu/pub?
    - [ ] some 403 forbiddens: openreview, some pub, e.g., https://www.cns.nyu.edu/pub/lcv/kadkhodaie24a.pdf
    - [ ] getting 403 on some dois? https://dx.doi.org/10.1152/jn.00900.2017
        - but then when I click on them manually no problem
    - [ ] all of jneurosci gives 404s for some reason
- [x] some of the abstracts include links to makeAbs.php, update
- [ ] Simoncelli96c RELATED? unsure what they mean
- [x] document "extras", in bibaux file and abstract folder
- [x] write a script to help validate input files?
    - check diffs, but I think it's largely unicode
