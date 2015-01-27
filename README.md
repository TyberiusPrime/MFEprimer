MFEprimer-2.0-tables
=================

MFEprimer command-line version source code

[Continue reading...](https://github.com/quwubin/MFEprimer/wiki/Manual)


This is a modification of the original MFEprimer-2.0 to use a pytables based
storage.
It needs a much smaller index (Drosphila: MFEprimer index: 2.7GB. MFEprimer-tables: 441MB),
indexes much faster (original: 24:07 minutes. -tables: 4:53), the PCR is slightly faster (0.5 vs 0.3 seconds),
and it does not require a rewritten fasta / two bit file - it can work with arbitrary fasta/2bit pairs.

Installation:
besides the MFEprimer install, you need to compile the dna2int module by visiting the chilli subdirectory
and doing python setup.py build_ext -i.

Index building:
With Index.py fasta_filename k (k = 9 is a decent value)

