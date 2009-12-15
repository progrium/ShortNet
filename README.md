ShortNet
=========
An extensible SMS-based BBS/wiki system

Dependencies
------------
Requires a Google Voice account and the Python libraries BeautifulSoup and simplejson (`easy_install BeautifulSoup simplejson`)

How it works
------------
When you run `python shortnet.py` it will ask you for your Google Account for 
Google Voice. Your Google Voice number is now a wiki service.

Using the Wiki
--------------
Get wiki pages by sending a text with the name of the page. Edit pages by sending a text with the name of the page, a space, and the content of the page. For example:

Texting `HelloWorld Hi! :)` to your number will create HelloWorld. You'll get a text back of the current version of the page, just as you'd see when you request it. Texting `HelloWorld` will get you the same response. The response includes a footer that has the author's number and when this page was last edited. For example, HelloWorld might look like this:

`Hi! :) 5551234/2s`

This shows the page was edited by 555-1234 about 2 seconds ago.

You can append content to a page by using the + modifier at the end of the page name. For example, after creating HelloWorld from the above, texting `HelloWorld+ Bye!` will return something like:

`Hi! :) Bye! 5551234/3s`

You have a special page using your phone number as the page name that only you can edit. Use it as a profile or public homepage. You have to create it first, so: `5551234 My homepage!`

Now go make lots of pages! Serve up microcontent over SMS. :)

Authors
-------
 * Adam Smith <adam@adamsmith.as>
 * Jeff Lindsay <progrium@gmail.com>

History
-------
ShortNet evolved from ShortWiki, a spontaneous one-night hack project at Hacker Dojo.

License
-------
MIT