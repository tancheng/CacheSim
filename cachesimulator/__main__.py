#!/usr/bin/env python3

import argparse

from cachesimulator.simulator import Simulator


# Parse command-line arguments passed to the program
def parse_cli_args():

    parser = argparse.ArgumentParser()

    # -------------------------------------------------------------------
    # l1 cache stats
    # -------------------------------------------------------------------
    parser.add_argument(
        '--l1-cache-size',
        type=int,
        required=True,
        help='the size of the l1 cache in words')

    parser.add_argument(
        '--l1-hit-latency',
        type=int,
        default=1,
        help='the access hit latency of l1 cache')

    parser.add_argument(
        '--l1-miss-latency',
        type=int,
        default=20,
        help='the access miss latency of l1 cache')

    parser.add_argument(
        '--l1-num-blocks-per-set',
        type=int,
        default=1,
        help='the number of blocks per set in l1')

    parser.add_argument(
        '--l1-num-words-per-block',
        type=int,
        default=1,
        help='the number of words per block in l1')

    parser.add_argument(
        '--l1-word-addrs',
        nargs='+',
        type=int,
        required=False,
        help='one or more base-10 word addresses in l1')

    parser.add_argument(
        '--l1-word-addrs-trace',
        required=False,
        help='base-10 word addresses trace file for l1')

    parser.add_argument(
        '--l1-write-miss-file',
        required=False,
        help='miss trace file for the next level of cache (i.e., l2 cache)')

    parser.add_argument(
        '--two-level',
        action='store_true',
        required=False,
        help='simulate a two-level cache hierarchy')

    parser.add_argument(
        '--l1-num-addr-bits',
        type=int,
        default=1,
        help='the number of bits in each given word address in l1')

    parser.add_argument(
        '--l1-replacement-policy',
        choices=('lru', 'mru'),
        default='lru',
        # Ignore argument case (e.g. "mru" and "MRU" are equivalent)
        type=str.lower,
        help='the l1 cache replacement policy (LRU or MRU)')

    # -------------------------------------------------------------------
    # l2 cache stats
    # -------------------------------------------------------------------
    parser.add_argument(
        '--l2-cache-size',
        type=int,
        required=False,
        help='the size of the l2 cache in words')

    parser.add_argument(
        '--l2-hit-latency',
        type=int,
        default=1,
        help='the access hit latency of l2 cache')

    parser.add_argument(
        '--l2-miss-latency',
        type=int,
        default=100,
        help='the access miss latency of l2 cache')

    parser.add_argument(
        '--l2-num-blocks-per-set',
        type=int,
        default=1,
        help='the number of blocks per set in l2')

    parser.add_argument(
        '--l2-num-words-per-block',
        type=int,
        default=1,
        help='the number of words per block in l2')

    parser.add_argument(
        '--l2-word-addrs',
        nargs='+',
        type=int,
        required=False,
        help='one or more base-10 word addresses in l2')

    parser.add_argument(
        '--l2-word-addrs-trace',
        required=False,
        help='base-10 word addresses trace file for l2')

    parser.add_argument(
        '--l2-write-miss-file',
        required=False,
        help='miss trace file for the next level of cache (i.e., l2 cache)')

    parser.add_argument(
        '--l2-num-addr-bits',
        type=int,
        default=1,
        help='the number of bits in each given word address in l2')

    parser.add_argument(
        '--l2-replacement-policy',
        choices=('lru', 'mru'),
        default='lru',
        # Ignore argument case (e.g. "mru" and "MRU" are equivalent)
        type=str.lower,
        help='the l2 cache replacement policy (LRU or MRU)')

    return parser.parse_args()

def main():

    cli_args = parse_cli_args()
    sim = Simulator()
    sim.run(cli_args.l1_num_blocks_per_set, cli_args.l1_num_words_per_block,
            cli_args.l1_cache_size,         cli_args.l1_replacement_policy,
            cli_args.l1_num_addr_bits,      cli_args.l1_word_addrs,
            cli_args.l1_word_addrs_trace,   cli_args.l1_hit_latency, 
            cli_args.l1_miss_latency,       cli_args.l1_write_miss_file)
    if cli_args.two_level:
        print("-------------------------------------------------------------")
        print("trying to simulate two level cache hierarchy")
        sim.run(cli_args.l2_num_blocks_per_set, cli_args.l2_num_words_per_block,
                cli_args.l2_cache_size,         cli_args.l2_replacement_policy,
                cli_args.l2_num_addr_bits,      cli_args.l2_word_addrs,
                cli_args.l1_write_miss_file,    cli_args.l2_hit_latency, 
                cli_args.l2_miss_latency)
    print("-------------------------------------------------------------")
    print("Completed simulation")

if __name__ == '__main__':
    main()
