from typing import Dict, List

from ModifyChain import load_translation_scheme
from utils import extract_reference_description, translate_dict, parse_fasta_dict, \
    FastaDictSeqEntry, parse_sq_bam, BamSeqEntry


def check_against_source_dict(chain_path: str, dict_path: str, translation_path: str = None) -> None:
    chain_source_dict, _ = extract_reference_description(chain_path)
    check_chain_against_dict(chain_source_dict, dict_path, translation_path)


def check_against_destination_dict(chain_path: str, dict_path: str, translation_path: str = None) -> None:
    _, chain_destination_dict = extract_reference_description(chain_path)
    check_chain_against_dict(chain_destination_dict, dict_path, translation_path)


def check_chain_against_dict(chain_dict: Dict[str, int], dict_path: str, translation_source_path: str = None) -> None:
    translation_source_dict: Dict[str, str] = {}
    if translation_source_path is not None:
        translation_source_dict = load_translation_scheme(translation_source_path)

    chain_dict = translate_dict(chain_dict, translation_source_dict)

    fasta_list: List[FastaDictSeqEntry] = parse_fasta_dict(dict_path)

    for entry in fasta_list:
        if entry.SN not in chain_dict:
            print("Would not be able to lift sequence: ", entry.SN)
        elif chain_dict[entry.SN] != entry.LN:
            print("Mismatching length data for: ", entry.SN, "length in chain is", chain_dict[entry.SN], "vs dict:",
                  entry.LN)


def check_chain_source_bam(chain_path: str, bam_path: str, translation_source_path: str = None) -> None:
    chain_source_dict, _ = extract_reference_description(chain_path)
    check_chain_against_bam(chain_source_dict, bam_path, translation_source_path)


def check_chain_against_bam(chain_dict: Dict[str, int], bam_path: str, translation_source_path: str = None) -> None:
    translation_source_dict: Dict[str, str] = {}
    if translation_source_path is not None:
        translation_source_dict = load_translation_scheme(translation_source_path)

    chain_dict = translate_dict(chain_dict, translation_source_dict)

    bam_list: List[BamSeqEntry] = parse_sq_bam(bam_path)

    for entry in bam_list:
        if entry.SN not in chain_dict:
            print("Would not be able to lift sequence: ", entry.SN)
        elif chain_dict[entry.SN] != entry.LN:
            print(
                "Mismatching length data for: ",
                entry.SN,
                "length in chain is",
                chain_dict[entry.SN],
                "vs dict:", entry.LN
            )
