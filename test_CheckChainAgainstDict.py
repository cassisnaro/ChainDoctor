from unittest import TestCase

from CheckChainAgainstDict import check_against_source_dict, check_against_destination_dict, check_chain_source_bam


class Test(TestCase):
    def test_check_chain_source_bam(self):
        result = check_chain_source_bam(
            chain_path = "TestMaterial/SimplifiedChain4.txt",
            bam_path = "TestMaterial/head_test.bam",
            translation_source_path = "TestMaterial/hg19_translation.txt"
        )
        self.assertSetEqual({'3','1'}, result.mismatching_length)
        self.assertSetEqual(
            {'GL000200.1', 'GL000242.1', 'GL000204.1', 'NC_007605', 'GL000224.1', '7', '2',
             'GL000235.1', 'GL000215.1', 'MT', 'GL000240.1', 'GL000191.1', 'GL000225.1',
             'GL000234.1', 'GL000229.1', 'GL000249.1', 'GL000218.1', 'GL000232.1', 'GL000231.1',
             'GL000217.1', 'GL000210.1', 'GL000219.1', 'GL000214.1', '19', '21', '13', 'GL000246.1',
             '9', '16', 'GL000233.1', 'GL000202.1', 'GL000195.1', 'GL000244.1', 'GL000206.1', '5',
             'GL000221.1', 'GL000208.1', '6', '11', '20', 'GL000245.1', 'GL000201.1', 'GL000243.1',
             'hs37d5', 'GL000228.1', '17', 'GL000248.1', 'GL000207.1', 'GL000220.1', 'GL000197.1',
             'GL000227.1', 'GL000196.1', 'GL000209.1', 'GL000212.1', 'GL000205.1', '22', '18',
             'GL000238.1', 'GL000239.1', 'X', 'GL000213.1', '12', 'GL000198.1', 'GL000230.1',
             'GL000236.1', 'GL000222.1', 'GL000223.1', 'GL000241.1', '15', 'GL000193.1', 'GL000216.1',
             '8', 'GL000199.1', 'GL000192.1', '14', '4', 'GL000203.1', '10', 'GL000247.1', 'GL000194.1',
             'GL000211.1', 'GL000226.1', 'GL000237.1'},
            result.missing_in_chain)
        self.assertSetEqual({'chrNoise'}, result.missing_in_dict)

    def test_check_against_destination_dict(self):
        result = check_against_destination_dict(
            chain_path = "TestMaterial/SimplifiedChain3.txt",
            dict_path = "TestMaterial/test.dict",
            translation_path = None)
        self.assertSetEqual({'chrY'}, result.mismatching_length)
        self.assertSetEqual({'chr1','chr2'}, result.missing_in_chain)
        self.assertSetEqual({'chrX'}, result.missing_in_dict)

    def test_check_against_source_dict(self):
        result = check_against_source_dict(
            chain_path = "TestMaterial/SimplifiedChain3.txt",
            dict_path = "TestMaterial/test.dict",
            translation_path = None)
        self.assertSetEqual({'chr1'}, result.mismatching_length)
        self.assertSetEqual({'chr2'}, result.missing_in_chain)
        self.assertSetEqual({'chr3'}, result.missing_in_dict)

    def test_check_to_string(self):
        result = check_against_source_dict(
            chain_path = "TestMaterial/SimplifiedChain3.txt",
            dict_path = "TestMaterial/test.dict",
            translation_path = None)
        self.assertEqual("""mismatching length information for sequences:
\tchr1
sequences present in the BAM/Dict but missing in the chain file:
\tchr2
sequences present in the chain file but missing in BAM/Dict file:
\tchr3
""", str(result))