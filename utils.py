import re

from typing import Dict, Tuple, List

import pysam

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
            q_end: int
    ):
        self.score = score
        self.t_name = t_name
        self.t_size = t_size
        self.t_strand = t_strand
        self.t_start = t_start
        self.t_end = t_end
        self.qName = q_name
        self.q_size = q_size
        self.q_strand = q_strand
        self.q_start = q_start
        self.q_end = q_end


def parse_chain_header(line: str) -> ChainHeaderLine:
    score, t_name, t_size, t_strand, t_start, t_end, q_name, q_size, q_strand, q_start, q_end, missing = parse_header(
        line)

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
        q_end
    )


def extract_reference_description(chain_path: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    source_info: Dict[str, int] = {}
    destination_info: Dict[str, int] = {}

    with open(chain_path) as chain_file:
        for line in chain_file:
            if line.startswith("chain"):
                parsed_header = parse_chain_header(line)

                if parsed_header.t_name not in source_info:
                    source_info[parsed_header.t_name] = parsed_header.t_size
                if parsed_header.t_size != source_info[parsed_header.t_name]:
                    raise Exception("inconsistency for source sequence ", parsed_header.t_name)

                if parsed_header.qName not in destination_info:
                    destination_info[parsed_header.qName] = parsed_header.q_size
                if parsed_header.q_size != destination_info[parsed_header.qName]:
                    raise Exception("inconsistency for destination sequence ", parsed_header.t_name)

    return source_info, destination_info


def translate_chain(chain_path: str, destination_path: str, translation_source: Dict[str, str],
                    translation_destination: Dict[str, str]):
    with open(chain_path) as chain_file, open(destination_path, "w") as output:
        for line in chain_file:
            if line.startswith("chain"):
                score, t_name, t_size, t_strand, t_start, t_end, q_name, q_size, q_strand, q_start, q_end, missing \
                    = parse_header(line)

                t_name_to_write = t_name
                if t_name in translation_source:
                    t_name_to_write = translation_source[t_name]

                q_name_to_write = q_name
                if q_name in translation_destination:
                    q_name_to_write = translation_destination[q_name]

                output.write("chain {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}\n".format(
                    score,
                    t_name_to_write,
                    t_size,
                    t_strand,
                    t_start,
                    t_end,
                    q_name_to_write,
                    q_size,
                    q_strand,
                    q_start,
                    q_end,
                    missing
                ))
            else:
                output.write(line)


def translate_dict(original_dict: Dict[str, int], translation_dict: Dict[str, str]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for original_key, value in original_dict.items():
        key = original_key
        if key in translation_dict:
            key = translation_dict[key]
        result[key] = value
    return result


class FastaDictSeqEntry:
    def __init__(self, sn, ln, ur, m5):
        self.SN = sn
        self.LN = ln
        self.UR = ur
        self.M5 = m5


def parse_fasta_dict(fasta_dict_path: str) -> List[FastaDictSeqEntry]:
    result: List[FastaDictSeqEntry] = []

    with open(fasta_dict_path) as fasta_dict:
        for line in fasta_dict:
            if not line.startswith("@SQ"):
                continue

            sn: str = str(None)
            ln: int
            ur: str = str(None)
            m5: str = str(None)
            for element in line.split():
                if element.startswith("SN"):
                    sn = element.split(":")[1]
                if element.startswith("LN"):
                    ln = int(element.split(":")[1])
                if element.startswith("UR"):
                    ur = element.split(":")[1]
                if element.startswith("M5"):
                    m5 = element.split(":")[1]

            result.append(FastaDictSeqEntry(sn, ln, ur, m5))
    return result


class BamSeqEntry:
    def __init__(self, sn, ln):
        self.SN = sn
        self.LN = ln


def parse_sq_bam(bam_path: str) -> List[BamSeqEntry]:
    result: List[BamSeqEntry] = []

    bam_file = pysam.AlignmentFile(bam_path, "rb")
    header = bam_file.header
    for seq in header['SQ']:
        result.append(BamSeqEntry(seq['SN'], seq['LN']))

    return result


def truncate(chain_path: str, destination_path: str, sequences_to_erase: List[str]):
    keep = True

    with open(chain_path) as chain_file, open(destination_path, "w") as output:
        for line in chain_file:
            if line.startswith("chain"):
                header_match = chain_header_parser.match(line)
                t_name = header_match.group(2)

                if t_name in sequences_to_erase:
                    keep = False
                else:
                    keep = True
            if keep:
                output.write(line)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract_reference_description('hg19ToHg38.over.chain')
