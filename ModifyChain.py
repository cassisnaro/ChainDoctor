from typing import Dict, List, Set

from ChainFile import ChainFile

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

    chainFile = ChainFile(chain_input_path)
    chainFile.translate(
        translate_source_dict=translation_source_dict,
        translate_destination_dict=translation_destination_dict
    )
    chainFile.write(chain_output_path)

def truncate_main(chain_path: str, destination_path: str, sequences_to_erase_path: str):
    sequences_to_erase: Set[str] = set()
    with open(sequences_to_erase_path) as sequences_to_erase_file:
        for sequence_to_erase in sequences_to_erase_file:
            sequences_to_erase.add(sequence_to_erase.strip())
    chain_file = ChainFile(chain_path)
    chain_file.truncate(truncate_source=sequences_to_erase, truncate_destination=sequences_to_erase)
    chain_file.write(destination_path)