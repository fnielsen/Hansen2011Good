Hansen2011Good
==============
Code and some data files for the conference article:

    Good Friends, Bad News - Affect and Virality in Twitter".
    Lars Kai Hansen, Adam Arvidsson, Finn Årup Nielsen, Elanor Colleoni, Michael Etter.
    Future Information Technology 185, Part 1 in Communications in Computer and Information Science : 34-43. 2011 December. 
    The 2011 International Workshop on Social Computing, Network, and Services (SocialComNet 2011) 
    `Publishers version <https://link.springer.com/chapter/10.1007/978-3-642-22309-9_5>`_ |
    `Brede Wiki <http://neuro.compute.dtu.dk/wiki/Good_friends,_bad_news_-_affect_and_virality_in_Twitter>`_ | 
    `Scholia <https://tools.wmflabs.org/scholia/work/Q27681552>`_

Notes about the data analysis:

    Diffusion and emotion:  The effect of sentiment of retweeting.  Notes to an article by Lars Kai Hansen,
    Adam Arvidsson, Elanor Colleoni, Michael Etter and Finn Årup Nielsen.
    Finn Årup Nielsen.
    http://www2.compute.dtu.dk/pubdb/views/edoc_download.php/7007/pdf/imm7007.pdf

Description
-----------
- The data here was not originally made in a format for release and as such not very readable and not ready for execution as file are referenced to specific file locations.
- Twitter data was used for this study. Due to the Twitter's Terms of Service this data cannot be released. If you are really interested in that we may be able to transfer them within-lab-wise, e.g., if you come to DTU Cognitive Systems. The data was split in two:
 - Streaming data from Twitter's sprinkler in a Mongodb
 - sqlite database with COP15 data (rbb.sqlite-2010-02-18 on 322M)
- The data was analyzed with a combination of Python and R: Data and feature extraction, R for the statistical analysis.
- The stop word list used was one from the Brede Toolbox, http://neuro.compute.dtu.dk/software/brede/. The specific file is called stop_english1.txt and available from http://neuro.compute.dtu.dk/software/brede/code/brede/data/stop_english1.txt It contains 571 words.
- The sentiment word list references AFINN-111.txt. That list is available both as part of the afinn python package and distributed on its own. You find it here https://github.com/fnielsen/afinn/blob/master/afinn/data/AFINN-111.txt and in this zip file: http://www2.compute.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
- Further Python files exist that were used to download the data.

Issues
------
Please note there might be "issues" with the code:

- The published article reads "The present list associates 1.446 words with a valence between -5 and +5" in the description of the sentiment word list. This is an old version of the list of "AFINN", with a length that neither corresponds to the distributed AFINN-96 (1480 words) nor AFINN-111 (2477 words). 
