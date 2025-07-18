#!/usr/bin/env python

import sys
import subprocess
import bibtexparser
from bibtexparser.model import Field
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
aux = bibtexparser.parse_file(sys.argv[2], append_middleware=[m.NormalizeFieldKeys()])
for aux_entry in aux.entries:
    entry = library.entries_dict[aux_entry.key]
    for field in aux_entry.fields:
        entry.set_field(field)
# these are failed because they have duplicate keys, so just add them together
for block in aux.failed_blocks:
    aux_entry = block.ignore_error_block
    entry = library.entries_dict[aux_entry.key]
    fields = {}
    for field in aux_entry.fields:
        v = fields.get(field.key.lower(), [])
        v.append(field.value.strip('"').strip("'"))
        fields[field.key.lower()] = v
    for k, v in fields.items():
        entry.set_field(Field(k, '||'.join(v)))

# remove all comments
library.remove(library.comments)
bibtexparser.write_file(sys.argv[3], library,
                        append_middleware=[m.MergeNameParts(), m.MergeCoAuthors()])
# bibtexparser writes these warning comments, which confuse jekyll-scholar, so remove them
proc = subprocess.run(["grep", "-v", "% WARNING", sys.argv[2]], capture_output=True)
with open(sys.argv[2], "w") as f:
    f.write(proc.stdout.decode())
