# REGnames

To build the corpus described at Ferreira et al. (2016c), the following steps should be taken:

1. Download the corpus [here](https://ilk.uvt.nl/~tcastrof/regnames/)
2. Set the following paths at [properties.py](https://github.com/ThiagoCF05/ProperName/blob/main/properties.py)
  * **root_dir** path of the corpus directory
  * **webpages_dir** path where the webpages are
  * **parsed_dir** path where the parsed webpages are
  * **mentions_dir** path where the mentions should be saved 
3. Run the [build.py](https://github.com/ThiagoCF05/ProperName/blob/master/main/corpus_builder/build.py) python script

## Citation
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

**Creators:** Thiago Castro Ferreira, Emiel Krahmer and Sander Wubben

Tilburg center for Cognition and Communication Department - Tilburg University