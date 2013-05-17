#!/usr/bin/env python
import bayes
import feedparser
#bayes.spamTest()
ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
#vocabList,pSF,pNY=bayes.localWords(ny,sf)
#vocabList,pSF,pNY=bayes.localWords(ny,sf)
bayes.getTopWords(ny,sf)
