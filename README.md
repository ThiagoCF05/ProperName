# Proper name generation

Proper name generation is a seriously understudied phenomenon in automatic text generation. There are potentially many different ways in which a person can be referred to in a text using their name (*Barack Hussein Obama II*, *Barack Obama*, *Obama*, *President Obama*, etc.) and arguably a text that uses different naming formats in different conditions is more human-like than one that relies on a fixed strategy (e.g., always use the full name).

This project introduces a statistical model able to generate variations of a proper name by taking into account the person to be mentioned, the discourse context and individual variation. The model relies on the REGnames corpus, a dataset with 53,102 proper name references to 1,000 people in different discourse contexts.

## REGnames

The code to build the REGnames corpus is available [here](https://github.com/ThiagoCF05/ProperName/tree/master/main/corpus_builder).

### Citation
```Tex
@InProceedings{castroferreira-wubben-krahmer:2016:INLG,
  author    = {Castro Ferreira, Thiago  and  Wubben, Sander  and  Krahmer, Emiel},
  title     = {Towards proper name generation: a corpus analysis},
  booktitle = {Proceedings of the 9th International Natural Language Generation conference},
  month     = {September 5-8},
  year      = {2016},
  address   = {Edinburgh, UK},
  publisher = {Association for Computational Linguistics},
  pages     = {222--226},
  url       = {http://anthology.aclweb.org/W16-6636}
}
```

## EACL 2017

The script performed to obtain the results described at the EACL 2017 paper can be found [here](https://github.com/ThiagoCF05/ProperName/tree/master/main/eacl)

The models described at the paper are available [here](https://github.com/ThiagoCF05/ProperName/tree/master/main/eacl/models)

### Citation
```Tex
```

**Creators:** Thiago Castro Ferreira, Emiel Krahmer and Sander Wubben

Tilburg center for Cognition and Communication Department - Tilburg University