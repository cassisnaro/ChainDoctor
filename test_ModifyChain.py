from unittest import TestCase
from ModifyChain import truncate_main, load_translation_scheme, translate_chain_file


class Test(TestCase):
    def test_truncate_main(self):
        chain_path='TestMaterial/SimplifiedChain2.txt'
        destination_path='TestOutputs/ChainFileTruncatedSourceTestOutput.chain'
        sequences_to_erase_path='TestMaterial/SimplifiedChain2_truncated_source_to_erase.txt'

        expected_result_path = 'TestMaterial/SimplifiedChain2_truncated_source.txt'
        truncate_main(chain_path, destination_path, sequences_to_erase_path, sequences_to_erase_path)

        with open(expected_result_path) as input_file, open(destination_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )

    def test_load_translation_scheme(self):
        translation_scheme_path = 'TestMaterial/translation_scheme.txt'

        self.assertEqual({'chrY': 'testMaterial1'}, load_translation_scheme(translation_scheme_path))

    def test_translate_chain_file(self):
        chain_path='TestMaterial/SimplifiedChain2.txt'
        destination_path='TestOutputs/ChainFileTranslatedSourceTestOutput.chain'
        translation_scheme_path='TestMaterial/translation_scheme.txt'

        expected_result_path = 'TestMaterial/SimplifiedChain2_translated_source.txt'
        translate_chain_file(chain_path, destination_path, translation_scheme_path, translation_scheme_path)

        with open(expected_result_path) as input_file, open(destination_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )