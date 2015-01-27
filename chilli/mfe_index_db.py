#!/usr/bin/env python
from __future__ import division

import os
import sys
import datetime
import time
from optparse import OptionParser
import sqlite3
import FastaIterator
import numpy
import pyximport; pyximport.install()
import dna2int
import tables
import collections


def optget():
    '''parse options'''
    parser = OptionParser()
    parser.add_option("-f", "--file", dest = "filename", help = "DNA file in fasta to be indexed")
    parser.add_option("-k", "--k", dest = "k", type='int', help = "K mer , default is 9", default = 9)

    (options, args) = parser.parse_args()

    if not options.filename:
        print_usage()
        exit()	

    return options

def print_usage():
    print '''
%s: Index DB for MFEprimer-2.0

Usage:

    %s -f human.genomic -k 9

Author: Wubin Qu <quwubin@gmail.com>
Last updated: 2012-4-24
    ''' % (os.path.basename(sys.argv[0]), os.path.basename(sys.argv[0]))

DNA2int = dna2int.DNA2int
    


def store_index(output_filename, lookup_dict, contig_lengths, k):
    """Store the index in multiple files:
    header: Defines k and the records indexed. 
    We use a unified coordinate system, limited to 2**32 -1 bases,
    and the header lists the offset of each record in this coordinate system

    The second file is a (compressed) blz array of kmer start stop offsets
    offsets[kmer][0] is the start of the respective kmer, offsets[kmer][1] the end of it's run.
    if offsets[kmer][0] is -1 (2**32) that kmer was not present.
    

    """
    print 'writing header'
    op = open(output_filename + '.header','wb')
    op.write("k=%i\n" % k)
    for record_id, length in contig_lengths:
        op.write("%i:%s\n" % (length, record_id))
    op.close()


    class KmerOffsets(tables.IsDescription):
        kmer = tables.UInt32Col()
        start = tables.UInt32Col()
        stop = tables.UInt32Col()
    
    class Kmer(tables.IsDescription):
        pos = tables.UInt32Col()
    filename = output_filename + '.tables' 
    FILTERS = tables.Filters(complib='zlib', complevel=5)
    h5file = tables.open_file(filename, mode='w', title='test', filters=FILTERS)
    group = h5file.create_group("/","kmer_pos", '')
    table_offsets = h5file.create_table(group, 'offsets', KmerOffsets, '')
    table_positions = h5file.create_table(group, 'positions', Kmer, '')
    row_offset = table_offsets.row
    row_positions = table_positions.row
    i = 0
    out_offsets= []
    for kmer_id, positions in sorted(lookup_dict.items()):
        for p in positions:
            row_positions['pos'] = p
            row_positions.append()
        start = i
        i += len(positions)
        stop = i
        out_offsets.append((kmer_id, start, stop))
    table_offsets.append(out_offsets)
    table_offsets.cols.kmer.create_index()
    h5file.close()
   
def index(filename, k):
    ''''''
    start = time.time()
    print 'indexing', filename

    mer_count = 4**k

    dbname = '.'.join(filename.split('.')[:-1]) + '.mfe_index'

    kmer_lookup = collections.defaultdict(list)

    is_empty = False
    is_db_new = True
    contig_lengths = []
    total_offset = 0

    for record in FastaIterator.parse(open(filename)):
        is_empty = False
        print record.id
        start_time = time.time()
        fasta_seq = record.seq
        dna2int.update_lookup(kmer_lookup, fasta_seq, total_offset, k)
        contig_lengths.append((record.id, len(fasta_seq)))
        total_offset += len(fasta_seq)
        print '%i bp took %.2f seconds' % (len(fasta_seq), time.time() - start_time)
        
    store_index(dbname, kmer_lookup, contig_lengths, k)

    print "Time used: %s" % str(time.time() - start)
    print 'Done.'

def main():
    '''main'''
    options = optget()
    index(options.filename, options.k)

if __name__ == "__main__":
    main()
