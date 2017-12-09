Findtelligent
=============

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/logo.png "Logo")

What is Findtelligent?
----------------------

Findtelligent is the smart substitute of browser's CTRL + F. No more exact matches! It gives you the possibility of executing queries (as in a Search Engine) to find information in a large HTML.

Findtelligent is composed of two parts. An API for functionality and a Chrome Extension for usability.

1. __API__: it allows you to get the most relevant passages in an HTML document based on a query.

2. __Chrome Extension__: it allows you to submit your query and automatically call the API, execute the query and highlight the relevant passages in the HTML in real time.

Why Findtelligent?
------------------

Usually Ctrl + F is not enough when searching the web. It uses an exact match instead of a free open query. 

Sometimes you are struggling with a huge HTML document such as a Wiki article, a User Guide, or even an e-book. With Findtelligent you can use a query instead of an exact match and get the passages that more likely contain the answer to your query.

What is Findtelligent's architecture?
-------------------------------------

The API was written using Python's Flask library. It follows a scalable and arranged workflow that allows any developer to implement a different passage retrieval method for scoring.

So far, the only method implemented for passage retrieval is called Density Distribution [1]. This passage retrieval technique allows to score the passages and return a set of passages that most likely contain the answer to the query.

Kise, Junke, Dengel, and Matsumoto [1] proposed a method to retrieve the most important passages based on local maximums of a density distribution which makes use of a fixed size window and TF-IDF techniques. In this case, since there is no a whole collection of documents but just one big HTML, then IDF was substituted for a made up measurement called IPF (Inverse Passage Frequency).

Below you can find a high-level block diagram of the structure of the software. It shows the /getbyurl API functionality which is the only one implemented so far. In the future a /getbyhtml should be included because some URLs are private and the API won't be able to retrieve the HTML in those cases, so the HTML itself must be passed in the body of the request.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/BlockDiagram.png "Block Diagram of Findtelligent API")

The Chrome Extension communicates the query, the URL of the HTML, and the scoring method to the API. The Flask route gets the request and pass the information of the URL to an HTML parser which retrieves the HTML using Beautiful Soup and urllib and transforms it to a plain text document. This plain text document and the query are passed to a passage retriever module which divides it into smaller passages based on a window size.

Both, the query and the passages created by the passage retriever, go through a tokenizer module which removes stopwords and stemmize the words using NLTK. The passage retriever also generates a simplified version of the passages by getting rid of those passages that don´t include any query term. The idea is to save time.

The simplified and tokenized passage list combined with the tokenized query go to a searching module which uses Whoosh library to index and score. The score function is a customized implementation that follows the algorithm proposed by Kise, Junke, Dengel, and Matsumoto [1].

Once all the scores are ready then a results parser is used to decide which are the relevant passages. In the case of density distribution algorithm all the local maximums are candidates to be relevant passages. Only the X percentile values are taken into consideration. This is easily tweakable by using an input variable.

Once the results list is ready (it's a list of passage IDs), the passasge retriever is used again to get all the relevant passages in a RegEx form. The RegEx form is ideal to highlight the passages in the original HTML without problem.

Finally the data is parsed in JSON format to be delivered by the API. Following you can see the API request and the API response.

Request:

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/RequestAPI.png "GetByUrl request API")

Response:

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/ResponseAPI.png "GetByUrl response API")

Notice the RegEx form on the response which is really useful to highlight the HTML using Mark.js library.

What about the Chrome Extension?
--------------------------------

The Chrome Extension is composed by two components:

1. Popup logic
2. Content logic

The popup logic includes an HTML and a JS file. The HTML is an extremely simple Front End with a blank space and a submit button so the user can enter a query and submit it. The JS will listen to a "click" or "enter key" event and execute an API call based on the information of the current tab. By now the API call is done to localhost. This can be easily change to point to any public host if the API wants to be publicly available.

Once the call is answered, a message is sent to what Chrome's developers called a content script.

The content logic is composed by a content JS and Mark.js library. The content JS is listening to messages from the popup JS. Once it receives a message it will use Mark.js to highlight the relevant passages using the RegEx form coming from the API. This is the easiest way to avoid problems with weird characters.

Below you can see an example. We are trying to find the "awards received by Vint Cerf" on a Wikipedia page. Notice the highlighted information after submitting the request.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/FindtelligentCapture.png "Findtelligent on action")

How to install?
---------------

There are two independent elements in Findtelligent: the API and the Chrome Extension.

* __API__: to install the API you'll need Python 3.6.2 and a web server. A Python [virtual environment](http://libzx.so/main/learning/2016/03/13/best-practice-for-virtualenv-and-git-repos.html) is recommended to avoid any confusion with old installed libraries.
    * Python: Please use the requirements.txt file to install the Python libraries (`$pip3 install -r requirements.txt`) instead of doing it manually. You'll also need to install some stopwords packets for NLTK (`$python -m nltk.downloader punkt stopwords`). Some of the libraries you'll need are:
        * Beautifulsoup 4
		* Flask
		* NLTK
		* Requests
		* Urllib
		* Whoosh
	* Web server: Flask can run using a web server or as developer mode. If you want to install a fixed instance of Findtelligent API you must install a web server or use a hosting option. Flask documentation explains how to do it using Apache, Nginx, etc. [here](http://flask.pocoo.org/docs/0.12/deploying/#self-hosted-options). You can also consider use other hosting options like Heroku by following [these](http://flask.pocoo.org/docs/0.12/deploying/#hosted-options) instructions.

* __Chrome Extension__: the Chrome Extension is still not publicly available on the Market Place because there is still no a fixed public instance of the API. Then, in order to install the extension locally you'll need to follow [these](https://developer.chrome.com/extensions/getstarted#unpacked) instructions.

How to use it?
--------------

Since there is no a fixed and public instance of the API yet, then you'll need to run the API locally. To do this you must follow these steps:

1. Open your virtual environment for Python 3.6.2 `$source ~/.yourEnvs/findtelligent/bin/activate` (you first need to set it up like [here](http://libzx.so/main/learning/2016/03/13/best-practice-for-virtualenv-and-git-repos.html)).
2. Clone the repository and go to the root directory of it.
3. Export the following Flask variables: `$export FLASK_APP=findelligentApi.py` and `$export FLASK_DEBUG=1`.
4. Run Flask's developer mode web server: `$python -m flask run`. You should see something like the image below.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/Flask.png "Flask execution")

5. Now you have a local instance of the API running. It's time to open Chrome and install the extension by following [these](https://developer.chrome.com/extensions/getstarted#unpacked) instructions. The directory that you need to select when click on "Load Unpacked extension..." is the `chrome_extension` directory in the repo. You should see something similar as below:

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/Extension.png "Chrome Extension")

6. Go to any public website. Click on the Findtelligent icon and write a query as shown below.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/FindtelligentIcon.png "Click icon")

7. Click submit or press enter and wait for a bit (__don't click on any other Chrome's tab while the process is running, if you do so you'll lose the results__). If there are possible answers for your query you'll see them highlighted. In the example below we looked for "Vint Cerf awards" in his Wikipedia page.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/Example.png "Example")

Evaluation
----------

No similar tools were found to compare with Findtelligent. The closest way to evaluate Findtelligent is by comparing the use of CTRL + F and Findtelligent. The difference is extremely intuitive, and both can be used for different goal, so there is no a quantitative method to compare them.

Let's inspect one use case for qualitative comparison. Let's say that you'd like to find the causes of extinction in a Wikipedia Evolution article. You can type on Findtelligent "Extinction causes" and get passages that are likely related to the topic. Below you can see some examples of the output.

![alt text](https://github.com/fvargaspiedra/findtelligent/blob/master/docs/Example2.png "Example 2")

There is no way to find that answer by using CTRL + F. The closest way would be to first try to look for the word Extinction and going over each match to find if it talks about extinction causes. This is precisely the kind of issues Findtelligent is meant to solve.

What should be improved?
------------------------

Even though the list of improvements is big, the idea is innovative and can be extrapolated to other use cases. There is no something alike out there, so the project worth to continue its development until reach a mature point.

* The scoring process must be done using parallel processing. Map Reduce it's a good candidate.
* Implement getbyhtml in the API. Currently only getbyurl is implemented, which means that the API is retrieving the HTML locally. This is not good in a case where the URL is private because the API is not going to be able to get the HTML, therefore, a new API endpoint must allow to pass the HTML directly in the body of the request.
* Add exceptions handling.
* Add logging functionality to the API.
* Add a "Find Next" button in the Chrome Extension so you can easily go to the highlighted sections.
* Add query processing status to the extension so the user can know whether the query was submitted and are waiting to get the answer from the API.
* Support for other languages (not only English).
* Add "question type" phase to understand what kind of question the query is trying to answer. This will give more accurate results.

References
----------

[1] K. Kise, M. Junker, A. Dengel, and K. Matsumoto. Passage Retrieval Based on Density Distributions of Terms and Its Applications to Document Retrieval and Question Answering. Reading and Learning, pp.306-327, 2004.
