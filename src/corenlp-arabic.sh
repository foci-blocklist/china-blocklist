java -Xmx3g -cp "../lib/corenlp/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-serverProperties StanfordCoreNLP-arabic.properties \
-preload tokenize,ssplit,pos,lemma,ner,parse \
-status_port 9001  -port 9001 -timeout 15000
