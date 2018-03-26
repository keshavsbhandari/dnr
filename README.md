This is an approach to text recommendation based on
word embeddings obtained from gensim model that can be build using gensim

https://radimrehurek.com/gensim/

After obtaining word2vec embeddings, This library will return you
best recommendation text out of collections of text such that text that was read by
user is already provided


This project is a part of my research for text based recommendation

W   

    =   [
        [w1, w2, ....... ],
        [w1, w2, ..............],
        [w1,w2,  ...................],
        ....
        ....
        ]

above document can be converted into vector from using word2vec model

V   

    =   word2vec(W)
    =   [
        [v1, v2, ....... ],
        [v1, v2, ..............],
        [v1, v2, ...................],
        ....
        ....
        ]
Calculating tf-idf score for each words in document

T   

    =   tfidf(V)

    =   [
        [t1, t2, ....... ],
        [t1, t2, ..............],
        [t1, t2, ...................],
        ....
        ....
        ]

Getting vector using Hadamard product of V and T

VT  

    =   [
        [v1 o t1, v2 o t2, ....... ],
        [v1 o t1, v2 o t2, ..............],
        [v1 o t1, v2 o t2, ...................],        
        ....
        ....
        ]

Now calculating the mean each sentence in VT


VT_   

      =   [
          mean([v1 o t1, v2 o t2, ....... ]),
          mean([v1 o t1, v2 o t2, ..............]),
          mean([v1 o t1, v2 o t2, ...................]),        
          ....
          ....
          ]
Now getting mean of VT_ which represents the mean of user digested news

V_  

      =   mean(VT_)

Now Suppose S is the collection of news from where recommendation is to be made we can convert it into vector represents using word2vec using following

S   

      =   [
          [v1, v2, ....... ],
          [v1, v2, ..............],
          [v1, v2, ...................],
          ....
          ....
          ]

Now we can measure similarity

sim(S,V_)   

            =   [
                [score],
                [score],
                [score],
                ....
                ....
                ]
Now depending upon the top score news can be recommended

This is just an implementation of my research for building content-based recommendation engine using word2vec model obtain from RNN
