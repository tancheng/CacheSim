#!/usr/bin/env python3

import math
import shutil

from cachesimulator.bin_addr import BinaryAddress
from cachesimulator.cache import Cache
from cachesimulator.reference import Reference
from cachesimulator.reference import ReferenceCacheStatus
from cachesimulator.table import Table

# The names of all reference table columns
REF_COL_NAMES = ('WordAddr', 'BinAddr', 'Tag', 'Index', 'Offset', 'Hit/Miss')
# The minimum number of bits required per group in a prettified binary string
MIN_BITS_PER_GROUP = 3
# The default column width of the displayed results table
DEFAULT_TABLE_WIDTH = 80


class Simulator(object):

    # Retrieves a list of address references for use by simulator
    def get_addr_refs(self, word_addrs, num_addr_bits,
                      num_offset_bits, num_index_bits, num_tag_bits):

        return [Reference(
                word_addr, num_addr_bits, num_offset_bits,
                num_index_bits, num_tag_bits) for word_addr in word_addrs]

    # Write the miss addresses into a file for the next level of cache
    def write_miss_refs(sef, write_miss_file, refs):
        with open(write_miss_file, "w") as file:
            for ref in refs:
                if ref.cache_status == ReferenceCacheStatus.miss:
                    file.write(str(ref.org_addr)+"\n")

    # Displays details for each address reference, including its hit/miss
    # status
    def display_addr_refs(self, refs, table_width):

        table = Table(
            num_cols=len(REF_COL_NAMES), width=table_width, alignment='right')
        table.header[:] = REF_COL_NAMES

        for ref in refs:

            if ref.tag is not None:
                ref_tag = ref.tag
            else:
                ref_tag = 'n/a'

            if ref.index is not None:
                ref_index = ref.index
            else:
                ref_index = 'n/a'

            if ref.offset is not None:
                ref_offset = ref.offset
            else:
                ref_offset = 'n/a'

            # Display data for each address as a row in the table
            table.rows.append((
                ref.word_addr,
                BinaryAddress.prettify(ref.bin_addr, MIN_BITS_PER_GROUP),
                BinaryAddress.prettify(ref_tag, MIN_BITS_PER_GROUP),
                BinaryAddress.prettify(ref_index, MIN_BITS_PER_GROUP),
                BinaryAddress.prettify(ref_offset, MIN_BITS_PER_GROUP),
                ref.cache_status))

        print(table)

    # Displays the contents of the given cache as nicely-formatted table
    def display_cache(self, cache, table_width):

        table = Table(
            num_cols=len(cache), width=table_width, alignment='center')
        table.title = 'Cache'

        cache_set_names = sorted(cache.keys())
        # A cache containing only one set is considered a fully associative
        # cache
        if len(cache) != 1:
            # Display set names in table header if cache is not fully
            # associative
            table.header[:] = cache_set_names

        # Add to table the cache entries for each block
        table.rows.append([])
        for index in cache_set_names:
            blocks = cache[index]
            table.rows[0].append(' '.join(
                ','.join(map(str, entry['data'])) for entry in blocks))

        print(table)
        print("total latency: ", cache.total_latency)

    # Run the entire cache simulation
    def run(self, num_blocks_per_set, num_words_per_block,
            cache_size, replacement_policy, num_addr_bits,
            word_addrs, word_addrs_trace,
            hit_latency, miss_latency, write_miss_file=None):

        if word_addrs_trace:
            new_words = []
            with open(word_addrs_trace) as file:
                for line in file: 
                    line = line.strip() #or some other preprocessing
                    new_words.append(int(line))
            print(new_words)
            word_addrs = new_words

        num_blocks = cache_size // num_words_per_block
        num_sets = num_blocks // num_blocks_per_set

        # Ensure that the number of bits used to represent each address is
        # always large enough to represent the largest address
        num_addr_bits = max(num_addr_bits, int(math.log2(max(word_addrs))) + 1)

        num_offset_bits = int(math.log2(num_words_per_block))
        num_index_bits = int(math.log2(num_sets))
        num_tag_bits = num_addr_bits - num_index_bits - num_offset_bits

        refs = self.get_addr_refs(
            word_addrs, num_addr_bits,
            num_offset_bits, num_index_bits, num_tag_bits)

        cache = Cache(
            num_sets=num_sets,
            num_index_bits=num_index_bits)

        cache.read_refs(
            num_blocks_per_set, num_words_per_block,
            replacement_policy, refs, hit_latency, miss_latency)

        # The character-width of all displayed tables
        # Attempt to fit table to terminal width, otherwise use default of 80
        table_width = max((shutil.get_terminal_size(
            (DEFAULT_TABLE_WIDTH, None)).columns, DEFAULT_TABLE_WIDTH))

        if write_miss_file:
          self.write_miss_refs(write_miss_file, refs)

        print()
        self.display_addr_refs(refs, table_width)
        print()
        self.display_cache(cache, table_width)
        print()
