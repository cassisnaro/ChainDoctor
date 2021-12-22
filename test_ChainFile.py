from unittest import TestCase

from ChainFile import ChainFile


class TestChainFile(TestCase):
    def test_read(self):
        chain_file = ChainFile("TestMaterial/SimplifiedChain.txt")
        self.assertEqual(2, len(chain_file.chains))

        header0 = chain_file.chains[0][0]
        entries0 = chain_file.chains[0][1]

        self.assertEqual(11867, header0.score)
        self.assertEqual("chrY", header0.t_name)
        self.assertEqual(59373566, header0.t_size)

        self.assertEqual(2, len(entries0))

        header1 = chain_file.chains[1][0]
        entries1 = chain_file.chains[1][1]

        self.assertEqual(10861, header1.score)
        self.assertEqual("chrY", header1.t_name)
        self.assertEqual(59373566, header1.t_size)

        self.assertEqual(2, len(entries1))

    def test_translate(self):
        test_check_input_path = "TestMaterial/SimplifiedChain_translated.txt"
        output_path = "TestOutputs/ChainFileTranslationTestOutput.chain"

        chain_file = ChainFile("TestMaterial/SimplifiedChain.txt")
        chain_file.translate({'chrY': "TestContent1"}, {'chrY': "TestContent2", 'chrX': "TestContent3"})
        chain_file.write(output_path)

        with open(test_check_input_path) as input_file, open(output_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )

    def test_translate_empty(self):
        test_check_input_path = "TestMaterial/SimplifiedChain_translated.txt"
        output_path = "TestOutputs/ChainFileTranslationTestOutput.chain"
        chain_file_path = "TestMaterial/SimplifiedChain.txt"

        chain_file = ChainFile(chain_file_path)
        chain_file.translate()
        chain_file.write(output_path)

        with open(chain_file_path) as input_file, open(output_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )

    def test_truncate_source_empty(self):
        test_check_input_path = "TestMaterial/SimplifiedChain2.txt"
        output_path = "TestOutputs/ChainFileTranslationTestOutput.chain"

        chain_file = ChainFile("TestMaterial/SimplifiedChain2.txt")
        chain_file.truncate()
        chain_file.write(output_path)

        with open(test_check_input_path) as input_file, open(output_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )

    def test_truncate_source_and_destination(self):
        test_check_input_path = "TestMaterial/SimplifiedChain2_truncated.txt"
        output_path = "TestOutputs/ChainFileTranslationTestOutput.chain"

        chain_file = ChainFile("TestMaterial/SimplifiedChain2.txt")

        truncate_source = set()
        truncate_source.add('chrY')
        truncate_destination = set()
        truncate_destination.add('chrX')

        chain_file.truncate(truncate_source=truncate_source, truncate_destination=truncate_destination)
        chain_file.write(output_path)

        with open(test_check_input_path) as input_file, open(output_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )

    def test_extract_reference_description(self):
        chain_file = ChainFile("TestMaterial/SimplifiedChain.txt")
        self.assertEqual(
            ({'chrY': 59373566}, {'chrY': 57227415, 'chrX': 156040895}),
            chain_file.extract_reference_description()
        )

    def test_write(self):
        input_path = "TestMaterial/SimplifiedChain.txt"
        output_path = "TestOutputs/ChainFileTestWriteOutput.chain"

        chain_file = ChainFile(input_path)
        chain_file.write(output_path)

        with open(input_path) as input_file, open(output_path) as output_file:
            self.assertEqual(
                input_file.read(),
                output_file.read()
            )
