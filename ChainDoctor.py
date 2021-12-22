#!/usr/bin/env python

import argparse
import sys

from CheckChainAgainstDict import check_against_destination_dict, check_against_source_dict, check_chain_source_bam
from ModifyChain import translate_chain_file, truncate_main


class ChainDoctor(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Utility to check and modify LiftOver chains',
            usage='''chaindoctor <command> [<args>]

The commands are:
   translate                    Changes sequences names in chain
   truncate                     Erases sequence information from chain
   check_source_against_dict       Checks if the source information in the chain is consistent with a FASTA dict
   check_destination_against_dict  Checks if the destination information in the chain is consistent with a FASTA dict
   check_source_against_bam        Checks if the source information in the chain is consistent with BAM file
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @staticmethod
    def translate():
        parser = argparse.ArgumentParser(
            description='Translate sequences names')
        parser.add_argument('-c', '--chain', required=True)
        parser.add_argument('-o', '--output', required=True)
        parser.add_argument('-s', '--source_translation', required=True)
        parser.add_argument('-d', '--destination_translation', required=True)

        args = vars(parser.parse_args(sys.argv[2:]))

        translate_chain_file(
            args['chain'],
            args['output'],
            args['source_translation'],
            args['destination_translation']
        )

    @staticmethod
    def truncate():
        parser = argparse.ArgumentParser(
            description='Translate sequences names')
        parser.add_argument('-c', '--chain', required=True)
        parser.add_argument('-o', '--output', required=True)
        parser.add_argument('-s', '--truncateSource', required=False)
        parser.add_argument('-d', '--truncateDestination', required=False)

        args = vars(parser.parse_args(sys.argv[2:]))

        truncate_main(
            chain_path=args['chain'],
            destination_path=args['output'],
            source_sequences_to_erase_path=args['truncateSource'],
            destination_sequences_to_erase_path=args['truncateDestination']
        )

    @staticmethod
    def check_destination_against_dict():
        parser = argparse.ArgumentParser(
            description='Checks if the destination information in the chain is consistent with a FASTA dict')
        parser.add_argument('-c', '--chain', required=True)
        parser.add_argument('-d', '--dict', required=True)
        parser.add_argument('-t', '--translate', required=False)

        args = vars(parser.parse_args(sys.argv[2:]))

        print(check_against_destination_dict(
            chain_path=args['chain'],
            dict_path=args['dict'],
            translation_path=args['translate']
        ))

    @staticmethod
    def check_source_against_dict():
        parser = argparse.ArgumentParser(
            description='Checks if the source information in the chain is consistent with a FASTA dict')
        parser.add_argument('-c', '--chain', required=True)
        parser.add_argument('-d', '--dict', required=True)
        parser.add_argument('-t', '--translate', required=False)

        args = vars(parser.parse_args(sys.argv[2:]))

        print(check_against_source_dict(
            chain_path=args['chain'],
            dict_path=args['dict'],
            translation_path=args['translate']
        ))

    @staticmethod
    def check_source_against_bam():
        parser = argparse.ArgumentParser(
            description='Checks if the source information in the chain is consistent with BAM file')
        parser.add_argument('-c', '--chain', required=True)
        parser.add_argument('-b', '--bam', required=True)
        parser.add_argument('-t', '--translate', required=False)

        args = vars(parser.parse_args(sys.argv[2:]))

        print(check_chain_source_bam(
            chain_path=args['chain'],
            bam_path=args['bam'],
            translation_source_path=args['translate']
        ))


if __name__ == '__main__':
    ChainDoctor()
