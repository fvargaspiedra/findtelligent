Findtelligent
=============

What is Findtelligent?
----------------------

Findtelligent is composed of two parts. An API for functionality and a Chrome Extension for usability.

1. API: allow you to get the most relevant passages in an HTML document based on a query.

2. Chrome Extension: allow you to submit your query and automatically connects to the API, execute the query and highlight the relevant passages in the HTML in real time.

Why Findtelligent?
------------------

Usually Ctrl + F is not enough when searching the web. It uses an exact match instead of a free open query. 

Sometimes you are struggling with a huge HTML document such as a Wiki article, a User Guide, or even an e-book. With Findtelligent you can use a query instead of an exact match and get the passages that more likely to contain the answer to your query.

What is Findtelligent's architecture?
-------------------------------------

The API was written using Python's Flask library. It follows a scalable and arranged workflow that allows any developer to implement a different passage retrieval method for scoring.

So far, the only method implemented for passage retrieval is called Density Distribution [1]. This passage retrieval technique allows to score the passages and return a set of passages that most likely contain the answer to the query.

Kise, Junke, Dengel, and Matsumoto [1] proposed a method to retrieve the most important passages based on local maximums of a density distribution which makes use of a fixed size window and TF-IDF techniques. In this case, since there is no a whole collection of documents but just one big HTML, then IDF was substituted for a made up measurement called IPF (Inverse Passage Frequency).

Below you can find a high-level block diagram of the structure of the software. It shows the /getbyurl API functionality which is the only one implemented so far. In the future a /getbyhtml should be included because some URLs are private and the API won't be able to retrieve the HTML in those cases, so the HTML itself must be passed in the body of the request.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/BlockDiagram.png "Block Diagram of Findtelligent API")

The Chrome Extension communicates the query, the URL of the HTML, and the scoring method to the API. The Flask route gets the request and pass the information of the URL to an HTML parser which retrieves the HTML using Beautiful Soup and urllib and transforms it to a plain text document. This plain text document and the query are passed to a passage retriever module which divides it into smaller passages based on a window size.

Both, the query and the passages created by the passage retriever go through a tokenizer module which removes stopwords and stemmize the words using NLTK. The passage retriever also generates a simplified version of the passages by getting rid of those passages that don´t include any query term. The idea is to save time.

The simplified and tokenized passage list combined with the tokenized query go to a searching module which uses Whoosh library to index and score. The score function is a customized implementation that follows the algorithm proposed by Kise, Junke, Dengel, and Matsumoto [1].

Once all the scores are ready then a results parser is used to decide which are the relevant passages. In the case of density distribution algorithm all the local maximums are candidates to be relevant passages. Only the X percentile values are taken into consideration. This is easily tweakable by using an input variable.

Once the results list is ready (it's a list of passage IDs), the passasge retriever is used again to get all the relevant passages in a RegEx form. The RegEx form is ideal to highlight the passages in the original HTML without problem.

Finally the data is parsed in JSON format to be delivered by the API. Following you can see the API request and the API response.

Request:

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/RequestAPI.png "Block Diagram of Findtelligent API")

Response:

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/ResponseAPI.png "Block Diagram of Findtelligent API")

Notice the RegEx form on the response which is really useful to highlight the HTML using Mark.js library.

References
----------

[1] K. Kise, M. Junker, A. Dengel, and K. Matsumoto. Passage Retrieval Based on Density Distributions of Terms and Its Applications to Document Retrieval and Question Answering. Reading and Learning, pp.306-327, 2004.



Please run the following commands before using it:

python -m nltk.downloader punkt stopwords

This is a Chrome extension for smart finding in a single HTML document.
