# WSM Project 1: Ranking by Vector Space Models
###### WSM Project 1

This project search for top 10 relevant articles based on input queries among 7,034 English news collected from _reuters.com_. The retrieved results will be shown as `NewsID \t Similarity Score`, and these results will be ranked from top relevant to least relevant.
#### Example Output
```
TF Weighting + Cosine Similarity
News            Score
---------       ---------
News123256      0.48507125007266594
News119356      0.48507125007266594
News108578      0.4472135954999579
News120265      0.4472135954999579
News103117      0.38575837490522974
News101763      0.3768891807222045
News111959      0.3768891807222045
News115859      0.3768891807222045
News119746      0.3768891807222045
News122919      0.37267799624996495
-------------------------
```

## Execute Directly
```
$ python3 main.py --query '<querylist>'
```

## Command Format
```
$ python3 main.py -d <doc_list_folder> -w <weight_type> -r <relevance_type> -q '<querylist>' [-f]
```
* `-d`, `--doc`: Specify search target folder.
* `-w`, `--weight`: Specify weight type, for instance: `tf` or `tfidf`.
* `-r`, `--relevance`: Define how to measure similarity, `cs` stands for Cosine Similarity, `eu` stands for Euclidean Distance.
* `-q`, `--query`: Define searching query, words seperated by ` (space)`.
* `-f`, `--feedback`: add this argument if want to calculate pseudo feedback.

### Command Example
#### Vector Space Model with Different Weighting Schemes & Similarity Metrics
1. Term Frequency (TF) Weighting + Cosine Similarity<br/>
    ```
    $ python3 main.py -d EnglishNews -w tf -r cs -q 'trump biden taiwan china'
    ```
    <br/>
2. Term Frequency (TF) Weighting + Euclidean Distance<br/>
   ```
   $ python3 main.py -d EnglishNews -w tf -r eu -q 'trump biden taiwan china'
   ```
   <br/>
3. TF-IDF Weighting + Cosine Similarity<br/>
    ```
    $ python3 main.py -d EnglishNews -w tfidf -r cs -q 'trump biden taiwan china'
    ```
    <br/>
4. TF-IDF Weighting + Euclidean Distance<br/>
   ```
   $ python3 main.py -d EnglishNews -w tfidf -r eu -q 'trump biden taiwan china'
   ```
   <br/>

#### Relevance Feedback
```
$ python3 main.py -d EnglishNews -w tfidf -r cs -q 'trump biden taiwan china' -f
```
