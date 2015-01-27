def DNA2int(kmer):
    '''convert a sub-sequence/seq to a non-negative integer'''
    cdef int out
    out = 0
    for l in kmer:
        out = out << 2
        if l == 'A':
            pass
        elif l == 'C':
            out = out + 1
        elif l == 'G':
            out = out + 2
        elif l == 'T':
            out = out + 3
        else:
            raise ValueError("Unexpected base: %s" % l)
        #else (A or something else)
        #out = out + 0 -> wa can skip on this ;)

    return out


def update_lookup(kmer_lookup, fasta_seq, total_offset, k):
    i_max = len(fasta_seq) - k
    cdef int i = 0
    cdef str fseq = fasta_seq
    cdef str kmer = fseq[:k]
    cdef int out = 0
    while i < i_max:
        try:
            out = 0
            for l in kmer:
                out = out << 2
                if l == 'A':
                    pass
                elif l == 'C':
                    out = out + 1
                elif l == 'G':
                    out = out + 2
                elif l == 'T':
                    out = out + 3
                else:
                    raise ValueError("Unexpected base: %s" % l)
            kmer_id = out
        except ValueError:
            #print 'Unrecognized base: %s' % fasta_seq[i+k]
            # Skip the unrecognized base, such as 'N'
            i += 1
            kmer = kmer[1:] + fasta_seq[i+k-1]
            continue
        kmer_lookup[kmer_id].append(i+k-1 + total_offset)
        
        i += 1
        kmer = fseq[i:i + k]
        if i % 1000000 == 0:
            print '.', 
