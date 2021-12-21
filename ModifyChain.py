from typing import Dict, List

from utils import translate_chain, truncate

def load_translation_scheme(translation_scheme_path: str) -> Dict[str, str]:
    result: Dict[str, str] = {}

    with open(translation_scheme_path) as translation_scheme_file:
        for line in translation_scheme_file:
            translation = line.split()
            result[translation[0]] = translation[1]

    return result

def translate_chain_file(
        chain_input_path: str,
        chain_output_path: str,
        translation_source_path: str,
        translation_destination_path: str
):
    translation_source_dict = load_translation_scheme(translation_source_path)
    translation_destination_dict = load_translation_scheme(translation_destination_path)
    translate_chain(chain_input_path, chain_output_path, translation_source_dict, translation_destination_dict)

def truncate_main(chain_path: str, destination_path: str, sequences_to_erase_path: str):
    sequences_to_erase: List[str] = []
    with open(sequences_to_erase_path) as sequences_to_erase_file:
        for sequence_to_erase in sequences_to_erase_file:
            sequences_to_erase.append(sequence_to_erase.strip())
    truncate(chain_path, destination_path, sequences_to_erase)