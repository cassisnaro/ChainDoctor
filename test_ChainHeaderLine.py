from unittest import TestCase

from ChainFile import ChainHeaderLine


class TestChainHeaderLine(TestCase):
    def test_create_from_string(self):
        line = "chain 20851231461 chr1 249250621 + 10000 249240621 chr1 248956422 + 10000 248946422 2"
        header = ChainHeaderLine.create_from_string(line)

        self.assertEqual(20851231461,header.score)
        self.assertEqual("chr1",header.t_name)
        self.assertEqual(249250621,header.t_size)
        self.assertEqual('+',header.t_strand)
        self.assertEqual(10000,header.t_start)
        self.assertEqual(249240621,header.t_end)
        self.assertEqual("chr1",header.q_name)
        self.assertEqual(248956422,header.q_size)
        self.assertEqual('+',header.q_strand)
        self.assertEqual(10000,header.q_start)
        self.assertEqual(248946422,header.q_end)
        self.assertEqual("2",header.missing)

    def test_write(self):
        line = "chain 20851231461 chr1 249250621 + 10000 249240621 chr1 248956422 + 10000 248946422 2"
        header = ChainHeaderLine.create_from_string(line)
        self.assertEqual(line, str(header))
