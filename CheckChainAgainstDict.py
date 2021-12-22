from typing import Dict, List

from ModifyChain import load_translation_scheme
from utils import extract_reference_description, translate_dict, parse_fasta_dict, \
    FastaDictSeqEntry, parse_sq_bam, BamSeqEntry

class ResultCheck:
    def __init__(self):
        self.mismatching_length = set()
        self.missing_in_chain = set()
        self.missing_in_dict = set()

    def add_mismatching_length(self, sequence_name: str):
        self.mismatching_length.add(sequence_name)

    def add_missing_in_chain(self, sequence_name: str):
        self.missing_in_chain.add(sequence_name)

    def add_missing_in_dict(self, sequence_name: str):
        self.missing_in_dict.add(sequence_name)

    def __write_mismatching_length__(self) -> str:
        result = ""
        if len(self.mismatching_length) == 0:
            return result
        result += "mismatching length information for sequences:\n"
        for sequence in self.mismatching_length:
            result += "\t" + sequence + "\n"
        return result

    def __write_missing_in_chain__(self) -> str:
        result = ""
        if len(self.missing_in_chain) == 0:
            return result
        result += "sequences present in the BAM/Dict but missing in the chain file:\n"
        for sequence in self.missing_in_chain:
            result += "\t" + sequence + "\n"
        return result

    def __write_missing_in_dict__(self) -> str:
        result = ""
        if len(self.missing_in_dict) == 0:
            return result
        result += "sequences present in the chain file but missing in BAM/Dict file:\n"
        for sequence in self.missing_in_dict:
            result += "\t" + sequence + "\n"
        return result

    def __str__(self) -> str:
        result = ""
        result += self.__write_mismatching_length__()
        result += self.__write_missing_in_chain__()
        result += self.__write_missing_in_dict__()

        return result

def check_against_source_dict(chain_path: str, dict_path: str, translation_path: str = None) -> ResultCheck:
    chain_source_dict, _ = extract_reference_description(chain_path)
    return check_chain_against_dict(chain_source_dict, dict_path, translation_path)


def check_against_destination_dict(chain_path: str, dict_path: str, translation_path: str = None) -> ResultCheck:
    _, chain_destination_dict = extract_reference_description(chain_path)
    return check_chain_against_dict(chain_destination_dict, dict_path, translation_path)

def fasta_list_to_dict(fasta_list: List[FastaDictSeqEntry]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for entry in fasta_list:
        result[entry.SN] = entry.LN
    return result

def bam_list_to_dict(bam_list: List[BamSeqEntry]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for entry in bam_list:
        result[entry.SN] = entry.LN
    return result


def check_chain_against_dict(chain_dict: Dict[str, int], dict_path: str, translation_source_path: str = None) -> ResultCheck:
    translation_source_dict: Dict[str, str] = {}
    if translation_source_path is not None:
        translation_source_dict = load_translation_scheme(translation_source_path)

    chain_dict = translate_dict(chain_dict, translation_source_dict)

    fasta_list: List[FastaDictSeqEntry] = parse_fasta_dict(dict_path)
    fasta_dict = fasta_list_to_dict(fasta_list)

    result = ResultCheck()

    for fasta_seq, fasta_length in fasta_dict.items():
        if fasta_seq not in chain_dict:
            result.add_missing_in_chain(fasta_seq)
        elif fasta_length != chain_dict[fasta_seq]:
            result.add_mismatching_length(fasta_seq)
    for chain_seq, _ in chain_dict.items():
        if chain_seq not in fasta_dict:
            result.add_missing_in_dict(chain_seq)

    return result


def check_chain_source_bam(chain_path: str, bam_path: str, translation_source_path: str = None) -> ResultCheck:
    chain_source_dict, _ = extract_reference_description(chain_path)
    return check_chain_against_bam(chain_source_dict, bam_path, translation_source_path)


def check_chain_against_bam(chain_dict: Dict[str, int], bam_path: str, translation_source_path: str = None) -> ResultCheck:
    translation_source_dict: Dict[str, str] = {}
    if translation_source_path is not None:
        translation_source_dict = load_translation_scheme(translation_source_path)

    chain_dict = translate_dict(chain_dict, translation_source_dict)

    bam_list: List[BamSeqEntry] = parse_sq_bam(bam_path)
    bam_dict = bam_list_to_dict(bam_list)

    result : ResultCheck = ResultCheck()

    for bam_seq, bam_seq_length in bam_dict.items():
        if bam_seq not in chain_dict:
            result.add_missing_in_chain(bam_seq)
        elif bam_seq_length != chain_dict[bam_seq]:
            result.add_mismatching_length(bam_seq)
    for chain_seq, _ in chain_dict.items():
        if chain_seq not in bam_dict:
            result.add_missing_in_dict(chain_seq)

    return result
