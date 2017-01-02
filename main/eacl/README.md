# Evaluation

To generate the results of the automatic evaluation describe at Ferreira et al. (2017), the following steps should be performed:

1. Build REGnames corpus following the steps described [here](https://github.com/ThiagoCF05/ProperName/tree/master/main/corpus_builder) (the corpus provided in the webpage is already built)
2. In [properties.py](https://github.com/ThiagoCF05/ProperName/blob/main/properties.py), set the following paths:
  * **root_dir** spath of the corpus directory
  * **parsed_dir** path where the parsed webpages are
  * **mentions_dir** path where the mentions are
  * **evaluation_dir** path where the results should be saved
3. Perform the [run.py](https://github.com/ThiagoCF05/ProperName/blob/master/main/eacl/run.py) python script
4. Perform the [eval.py](https://github.com/ThiagoCF05/ProperName/blob/master/main/eacl/evaluation/eval.py) python script

## Citation

**Creators:** Thiago Castro Ferreira, Emiel Krahmer and Sander Wubben

Tilburg center for Cognition and Communication Department - Tilburg University