# Ranking-VSM

## Command Format
`main.py -d <doc_list_folder> -w <weight_type> -r <relevance_type> -q '<querylist>' [-f]`

### Vector Space Model with Different Weighting Schemes & Similarity Metrics
1. Term Frequency (TF) Weighting + Cosine Similarity<br/>
    `python3 main.py -d EnglishNews -w tf -r cs -q 'trump biden taiwan china'`<br/>
2. Term Frequency (TF) Weighting + Euclidean Distance<br/>
    `python3 main.py -d EnglishNews -w tf -r eu -q 'trump biden taiwan china'`<br/>
3. TF-IDF Weighting + Cosine Similarity<br/>
    `python3 main.py -d EnglishNews -w tfidf -r cs -q 'trump biden taiwan china'`<br/>
4. TF-IDF Weighting + Euclidean Distance<br/>
    `python3 main.py -d EnglishNews -w tfidf -r eu -q 'trump biden taiwan china'`<br/>

### Relevance Feedback
`python3 main.py -d EnglishNews -w tfidf -r cs -q 'trump biden taiwan china' -f`
