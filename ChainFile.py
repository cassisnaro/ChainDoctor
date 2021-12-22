from __future__ import annotations

import re
from typing import List, Tuple, Dict, Set
from itertools import filterfalse

chain_header_parser = re.compile(r'chain (\d*) ([\w.]*) (\d*) (.) (\d*) (\d*) (\w*) (\d*) (.) (\d*) (\d*) (\d*)')


def parse_header(header_line: str) -> tuple[int, str, int, str, int, int, str, int, str, int, int, str]:
    header_match = chain_header_parser.match(header_line)

    score = int(header_match.group(1))
    t_name = header_match.group(2)
    t_size = int(header_match.group(3))
    t_strand = header_match.group(4)
    t_start = int(header_match.group(5))
    t_end = int(header_match.group(6))
    q_name = header_match.group(7)
    q_size = int(header_match.group(8))
    q_strand = header_match.group(9)
    q_start = int(header_match.group(10))
    q_end = int(header_match.group(11))
    missing = header_match.group(12)

    return score, t_name, t_size, t_strand, t_start, t_end, q_name, q_size, q_strand, q_start, q_end, missing


class ChainHeaderLine:
    def __init__(
            self,
            score: int,
            t_name: str,
            t_size: int,
            t_strand: str,
            t_start: int,
            t_end: int,
            q_name: str,
            q_size: int,
            q_strand: str,
            q_start: int,
            q_end: int,
            missing: str
    ):
        self.score = score
        self.t_name = t_name
        self.t_size = t_size
        self.t_strand = t_strand
        self.t_start = t_start
        self.t_end = t_end
        self.q_name = q_name
        self.q_size = q_size
        self.q_strand = q_strand
        self.q_start = q_start
        self.q_end = q_end
        self.missing = missing

    @staticmethod
    def create_from_string(line: str) -> ChainHeaderLine:
        score, t_name, t_size, t_strand, t_start, t_end, q_name, q_size, q_strand, q_start, q_end, missing = \
            parse_header(line)

        return ChainHeaderLine(
            score,
            t_name,
            t_size,
            t_strand,
            t_start,
            t_end,
            q_name,
            q_size,
            q_strand,
            q_start,
            q_end,
            missing
        )

    def __str__(self):
        return "chain {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}".format(
                self.score,
                self.t_name,
                self.t_size,
                self.t_strand,
                self.t_start,
                self.t_end,
                self.q_name,
                self.q_size,
                self.q_strand,
                self.q_start,
                self.q_end,
                self.missing
            )


class ChainFile:
    def __init__(self, path: str):
        self.chains: List[Tuple[ChainHeaderLine, List[str]]] = []

        parsed_header: ChainHeaderLine | None = None
        parsed_entries: List[str] = []
        with open(path) as chain_file:
            for line in chain_file:
                if line.startswith("chain"):
                    if parsed_header is not None:
                        self.chains.append((parsed_header, parsed_entries))
                        parsed_entries: List[str] = []
                    parsed_header = ChainHeaderLine.create_from_string(line)
                elif len(line) > 2:
                    parsed_entries.append(line)
        if parsed_header is not None:
            self.chains.append((parsed_header, parsed_entries))

    def translate(self,
                  translate_source_dict: Dict[str, str] = None,
                  translate_destination_dict: Dict[str, str] = None):
        if translate_source_dict is None:
            translate_source_dict = {}
        if translate_destination_dict is None:
            translate_destination_dict = {}

        for chain in self.chains:
            t_name_new = chain[0].t_name
            if chain[0].t_name in translate_source_dict:
                t_name_new = translate_source_dict[chain[0].t_name]

            q_name_new = chain[0].q_name
            if chain[0].q_name in translate_destination_dict:
                q_name_new = translate_destination_dict[chain[0].q_name]

            chain[0].t_name = t_name_new
            chain[0].q_name = q_name_new

    def truncate(self,
                 truncate_source: Set[str] = None,
                 truncate_destination: Set[str] = None):
        if truncate_source is None:
            truncate_source = set()
        if truncate_destination is None:
            truncate_destination = set()
        self.chains[:] = filterfalse(
            lambda chain: chain[0].t_name in truncate_source or chain[0].q_name in truncate_destination,
            self.chains
        )





    def extract_reference_description(self) -> Tuple[Dict[str, int], Dict[str, int]]:
        source_info: Dict[str, int] = {}
        destination_info: Dict[str, int] = {}

        for header, _ in self.chains:
            if header.t_name in source_info:
                if source_info[header.t_name] != header.t_size:
                    raise Exception("Source information inconsistent for " + header.t_name)
            source_info[header.t_name] = header.t_size

            if header.q_name in destination_info:
                if destination_info[header.q_name] != header.q_size:
                    raise Exception("Destination information inconsistent for " + header.q_name)
            destination_info[header.q_name] = header.q_size

        return source_info, destination_info

    def write(self, chain_output_path):
        with open(chain_output_path, "w") as output_file:
            for header, entries in self.chains:
                output_file.write(str(header)+"\n")
                for entry in entries:
                    output_file.write(entry)
                output_file.writelines("\n")
