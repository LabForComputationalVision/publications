#!/usr/bin/env python

import argparse
import os
import pathlib

import bibtexparser
import bibtexparser.middlewares as m
from bibtexparser.model import Field

TRANSLATE_BRACKETS = str.maketrans({"{": r"\{", "}": r"\}"})


class AddFirstAuthor(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        author = entry.get("author")
        if author:
            author = author.value[0].last
            assert len(author) == 1
            author = author[0]
            if author[0] == "{":
                author = author[1:-1]
            # bug https://github.com/inukshuk/jekyll-scholar/issues/366
            for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                if author.startswith(month):
                    author = author.replace(month, f"{month[:2]}-{month[2]}")
            entry["first_author"] = author.replace("*", "")
        return entry


# some entries have a "type" field, which confuses the parser for ruby-bibtex
# (duplicate with "entry type", e.g., article, inproceedings)
class ConvertType(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        type_field = entry.pop("type")
        if type_field:
            entry["addt_type"] = type_field.value
        return entry


class AddOrigBibtex(m.BlockMiddleware):
    def transform_entry(self, entry, *args, **kwargs):
        entry["original_bibtex"] = entry.raw.translate(TRANSLATE_BRACKETS)
        return entry


class CorrectTilde(m.BlockMiddleware):
    # turn the bare tilde into the latex version, so it gets
    # rendered correctly by bibtex-ruby
    def transform_entry(self, entry, *args, **kwargs):
        for field in entry.fields:
            field.value = field.value.replace("~", r"\~{}")
        return entry


def main(
    bib: str,
    out: str,
    aux: str | None,
    abstracts: str | None,
    author_url: str | None,
    journal_url: str | None,
):
    additional_middleware = []

    if author_url is not None and os.path.exists(author_url):
        with open(author_url) as f:
            author_url = f.readlines()
        author_url = {
            a.split("=")[0].strip().replace(" ", ""):
            a.split("=")[1].strip().strip('"').strip("'")
            for a in author_url if a.strip()
        }

    class RenderAuthors(m.BlockMiddleware):
        def transform_entry(self, entry, *args, **kwargs):
            authors = entry.get("author")
            if authors:
                author_str = ""
                for i, author in enumerate(authors.value):
                    if url := author_url.get(author.replace(" ", "")):
                        author_str += f"<i><a href={url}>{author}</a></i>"
                    else:
                        author_str += f"<i>{author}</i>"
                    if i == len(authors.value) - 2:
                        author_str += " and "
                    elif i == len(authors.value) - 1:
                        author_str += "."
                    else:
                        author_str += ", "
                entry["rendered_author"] = author_str
            return entry

    additional_middleware.append(RenderAuthors())

    if journal_url is not None and os.path.exists(journal_url):
        with open(journal_url) as f:
            journal_url = f.readlines()
        journal_url = {
            j.split("=")[0].strip().replace(" ", "").lower():
            j.split("=")[1].strip().strip('"').strip("'")
            for j in journal_url if j.strip()
        }

    class RenderJournals(m.BlockMiddleware):
        def transform_entry(self, entry, *args, **kwargs):
            journal = entry.get("journal")
            if not journal:
                journal = entry.get("booktitle")
            if journal:
                journal = journal.value
                if url := journal_url.get(journal.replace(" ", "").lower()):
                    journal_str = f"<a href={url}>{journal}</a>"
                else:
                    journal_str = journal
                entry["rendered_journal"] = journal_str
            return entry

    additional_middleware.append(RenderJournals())

    if abstracts is not None:
        abstracts = pathlib.Path(abstracts)

        class AddAbstract(m.BlockMiddleware):
            def transform_entry(self, entry, *args, **kwargs):
                abstract_path = abstracts / f"{entry.key}-abstract.txt"
                if abstract_path.exists():
                    abstract = abstract_path.read_text()
                    entry["abstract"] = abstract
                return entry

        additional_middleware.append(AddAbstract())

    middlewares = [
        AddOrigBibtex(),
        m.NormalizeFieldKeys(),
        ConvertType(),
        m.SeparateCoAuthors(),
    ]
    middlewares += additional_middleware
    middlewares += [
        m.SplitNameParts(),
        AddFirstAuthor(),
        m.MergeNameParts(),
        m.MergeCoAuthors(),
        CorrectTilde(),
    ]
    library = bibtexparser.parse_file(bib, append_middleware=middlewares)
    if aux is not None and os.path.exists(aux):
        aux = bibtexparser.parse_file(
            aux,
            append_middleware=[m.NormalizeFieldKeys(), ConvertType(), CorrectTilde()],
        )
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
                v.append(field.value.strip('"').strip("'").replace("~", r"\~{}"))
                # turn the bare tilde into the latex version, so it gets
                # rendered correctly by bibtex-ruby
                fields[field.key.lower()] = v
            for k, v in fields.items():
                entry.set_field(Field(k, "||".join(v)))

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare bibtex file for jekyll site")
    parser.add_argument("bib", help="Path to the standard-formatted .bib file")
    parser.add_argument(
        "--out",
        "-o",
        default="site/_bibliography/references.bib",
        help="Path to save output at.",
    )
    parser.add_argument(
        "--aux",
        default=None,
        help="Path to the .bibaux file with additional info. See Readme for details.",
    )
    parser.add_argument(
        "--abstracts",
        default=None,
        help="Path to the folder containing abstract files. See Readme for details",
    )
    parser.add_argument(
        "--author_url",
        default=None,
        help="Path to the txt file containing author urls. See Readme for details",
    )
    parser.add_argument(
        "--journal_url",
        default=None,
        help="Path to the txt file containing journal urls. See Readme for details",
    )
    args = vars(parser.parse_args())
    main(**args)
