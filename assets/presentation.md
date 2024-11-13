---
author: Dyma Solovei
date: November 13, 2024
paging: Page %d of %d
---

# Cheating On Math Homework With A Vector Database


---

## Agenda

- Recap: Vector Databases
- **Calculating Euclidean distance with Weaviate**
- Bonus? (if time allows)
- Q&A

---

## Recap: Vector Databases

A vector database is ...

a specialized type of database...

designed to store and retrieve data objects based on their _semantic properties_ rather than the data itself...

by building indices on top of their vectorized representation.

<br>

##### What is it used for?

Almost anything can be transformed into a vector and stored in a vector database: text, images, audio, graphs, etc.

```
┌───────────────────────┐      ┌────────────────────────────┐
│ London is the capital │      │ [0.3,0.45,0.16,0.73,0.0205,│
│   of Great Britain    ├──────►  0.22,1.67,1.33,0.56,...]  │
└───────────────────────┘      └────────────────────────────┘
```



---

## Calculating Euclidean distance with Weaviate

##### Problem:

> It's 8pm and you're on the couch, browsing 9GAG after a long but fulfilling day at work.
> Your kid, who's recently moved to the 9th grade, shuffles in and asks you to help with their math homework.
> As the eyes brush the page, a look of dismay comes upon your face... it's **Vector Distances**.

<br>

Q: Can a Vector Database solve your problem?

A: Of course it can.

<br>

<br>

<br>

<br>

___

To prove it, let's build a simple CLI tool powered by a vector database.

---

### Prerequisites

1. A vector database -- [Weaviate](https://weaviate.io/developers/weaviate)

Weaviate _(we-vee-eight)_ is an open source database written in Go.

- Supports multi-modal search (text/vector/hybrid)
- Easy to run locally with Docker 🐋
- Comes with built-in embedding modules
- Has clients for Python, JS/TS, Java, and Go

2. Python environment

```sh
mkdir cheating-math-homework/ && cd cheating-math-homework/
virtualenv .venv
source .venv/bin/activate
```

3. ~~A kid~~

Contrary to your expectations, it will not require a kid.

---

### Vector Distance: recap

To calculate Euclidean distance between 2 vectors we:

<br>

- [x] Created a new collection and configured the vector index to use `l2-squared` vector distance.

```md
Other available distance metrics include `cosine`, `dot`, `hamming`, and `manhattan`.
```

<br>

- [x] Stored a new object to that collection and provided `v1` as our _custom vector_.

- [x] Used `near_vector` search to find the **closest object** to `v2` and fetched "distance" metadata as an additional parameter.

```md
Additional parameters like `id`, `certainty` and `score` provide more metadata on search results, while `rerank` can be used to reorder them.
```

<br>

Remember that we also had to take the square root of the returned distance.

---

## Bonus!

##### Problem:

> Our other child, still a toddler, will be taking an entrance exam to the kindergarten next week.

<br>

Q: Can a vector database get your kid into kindergarten too? 

A: ...

<br>

<br>

### "Which word does not belong?"

Commonly used to test children's ability to group objects by similarity, the game is a choice of several words, one of which is distinctly different from the others:

```
apple organge banana sponge
```
___

Let's extend our handy little tool and pit it against some examples from [Baamboozle](https://www.baamboozle.com/game/993946). 

---

### Words: recap

To find the "outlier" word we:

- [x] Enabled `text2vec-contextionary` module and ran Contextionary in a separate container

```md
Enabling more features is easy with Weaviate's "Configurator"
https://weaviate.io/developers/weaviate/installation/docker-compose#configurator
```

<br>

- [x] Created a new collection and configured a vectorizer for it.
- [x] Stored the words as separate objects, _letting the vectorizer do the job_.
- [x] Searched for `n-2` similar words using `near_text` search and counted their occurrences.
- [x] Found the word which was returned the least number of times.

---

## Q&A

```txt






                     _____       ____     ______     
                    /\  __`\   /|  _ \   /\  _  \    
                    \ \ \/\ \  |/\   |   \ \ \L\ \   
                     \ \ \ \ \  \// __`\/\\ \  __ \  
                      \ \ \\'\\ /|  \L>  <_\ \ \/\ \ 
                       \ \___\_\| \_____/\/ \ \_\ \_\
                        \/__//_/ \/____/\/   \/_/\/_/







```

---

## References

Me:

- github: [@bevzzz](https://github.com/bevzzz)
- x: [@dymasolovei](https://x.com/dymasolovei)
- tamtamy: [@dyma](https://tamtamy.reply.com/tamtamy/user/id-d.solovei.action)

Problem sets:

- [Vectors in Three Dimensions](https://math.libretexts.org/Bookshelves/Calculus/Calculus_(OpenStax)/12%3A_Vectors_in_Space/12.02%3A_Vectors_in_Three_Dimensions)
- [Baamboozled - Which Word Doesn't Belong?](https://www.baamboozle.com/game/993946)

Weaviate docs:

- [How-to: Connect](https://weaviate.io/developers/weaviate/connections/connect-local)
- [How-to: Manage data](https://weaviate.io/developers/weaviate/manage-data)
- [How-to: Vector Similarity Search](https://weaviate.io/developers/weaviate/search/similarity)
- [Contexttionary Vectorizer](https://weaviate.io/developers/weaviate/modules/text2vec-contextionary)

ASCII art:

- [ASCII Art Archive](https://www.asciiart.eu/text-to-ascii-art)
- [asciiflow](https://asciiflow.com)

___

This presentation and the code for this talk are available at: https://github.com/bevzzz/cheating-math-homework
