#!/usr/bin/env python

import sys
import subprocess
import bibtexparser
import bibtexparser.middlewares as m

class AddFirstAuthor(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        author = entry.get("author")
        if author:
            author = author.value[0].last
            assert len(author) == 1
            if author[0][0] == "{":
                author[0] = author[0][1:-1]
            entry["first_author"] = author[0]
        return entry

middlewares = [m.NormalizeFieldKeys(), m.SeparateCoAuthors(), m.SplitNameParts(), AddFirstAuthor()]
library = bibtexparser.parse_file(sys.argv[1],
                                  append_middleware=middlewares)
# remove all comments
library.remove(library.comments)
bibtexparser.write_file(sys.argv[2], library,
                        append_middleware=[m.MergeNameParts(), m.MergeCoAuthors()])
# bibtexparser writes these warning comments, which confuse jekyll-scholar, so remove them
proc = subprocess.run(["grep", "-v", "% WARNING", sys.argv[2]], capture_output=True)
with open(sys.argv[2], "w") as f:
    f.write(proc.stdout.decode())
