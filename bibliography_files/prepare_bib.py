#!/usr/bin/env python

import sys
import bibtexparser
import bibtexparser.middlewares as m

class FixKeys(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        for k in entry.fields_dict.keys():
            field = entry.pop(k)
            field.key = k.lower()
            entry.set_field(field)
        return entry

class AddFirstAuthor(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        author = entry.get("author")
        if author:
            author = author.value[0].last
            assert len(author) == 1
            entry["first_author"] = author[0]
        return entry

middlewares = [FixKeys(), m.SeparateCoAuthors(), m.SplitNameParts(), AddFirstAuthor()]
library = bibtexparser.parse_file(sys.argv[1],
                                  append_middleware=middlewares)
shortened = bibtexparser.Library(library.blocks[:10])
with open(sys.argv[2], "w") as f:
    f.write(bibtexparser.write_string(shortened))#, append_middleware=[m.MergeNameParts(), m.MergeCoAuthors()])
