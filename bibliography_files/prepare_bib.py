#!/usr/bin/env python

import pathlib
import argparse
import subprocess
import bibtexparser
from bibtexparser.model import Field
import bibtexparser.middlewares as m

TRANSLATE_BRACKETS = str.maketrans({"{": r"\{", "}": r"\}"})

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

# tech reports can have a "type" field, which confuses the parser for
# ruby-bibtex (duplicate with "entry type", e.g., article, inproceedings)
class ConvertTechReportType(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        type_field = entry.pop("type")
        if type_field:
            entry["techreport_type"] = type_field.value
        return entry

class AddOrigBibtex(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        entry["original_bibtex"] = entry.raw.translate(TRANSLATE_BRACKETS)
        return entry

def main(bib: str, out: str, aux: str | None,
         abstracts: str | None):

    if abstracts is not None:
        abstracts = pathlib.Path(abstracts)
        class AddAbstract(m.BlockMiddleware):
            def transform_entry(self, entry, *args, **kwargs):
                abstract_path = abstracts / f"{entry.key}-abstract.txt"
                if abstract_path.exists():
                    abstract = abstract_path.read_text()
                    entry["abstract"] = abstract
                return entry
        add_abstract = [AddAbstract()]
    else:
        add_abstract = []

    middlewares = [AddOrigBibtex(), m.NormalizeFieldKeys(), ConvertTechReportType()]
    middlewares += add_abstract
    middlewares += [m.SeparateCoAuthors(), m.SplitNameParts(), AddFirstAuthor(), m.MergeNameParts(),
                    m.MergeCoAuthors()]
    library = bibtexparser.parse_file(bib, append_middleware=middlewares)
    if aux is not None:
        aux = bibtexparser.parse_file(aux, append_middleware=[m.NormalizeFieldKeys()])
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

        # go through and add superseded_by to entries
        for entry in library.entries:
            if supersedes := entry.fields_dict.get("supersedes"):
                for old_entry in supersedes.value.split("||"):
                    old_entry = library.entries_dict[old_entry]
                    if superseded := old_entry.get("superseded_by"):
                        superseded = f"||{superseded.value}"
                    else:
                        superseded = ""
                    old_entry.set_field(Field("superseded_by", entry.key + superseded))

    # remove all comments
    library.remove(library.comments)
    bibtexparser.write_file(out, library)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare bibtex file for jekyll site")
    parser.add_argument("bib",
                        help="Path to the standard-formatted .bib file")
    parser.add_argument("--out", "-o", default="site/_bibliography/references.bib",
                        help="Path to save output at.")
    parser.add_argument("--aux", default=None,
                        help="Path to the .bibaux file with additional info. See Readme for details.")
    parser.add_argument("--abstracts", default=None,
                        help="Path to the folder containing abstract files. See Readme for details")
    args = vars(parser.parse_args())
    main(**args)
