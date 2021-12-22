from typing import Dict, Tuple, List

import pysam

from ChainFile import ChainFile


def extract_reference_description(chain_path: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    chain_file = ChainFile(chain_path)
    return chain_file.extract_reference_description()


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


if __name__ == '__main__':
    extract_reference_description('hg19ToHg38.over.chain')
