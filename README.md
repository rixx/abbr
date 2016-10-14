# abbr

abbr is a self-hosted URL shortener written in Python/flask.

## Current state

Expiry, authentication and a bookmarklet still need to be done. Install information, and packaging, too.

## Features

 - shorten a URL in the web interface, optionally give a custom short name
 - use `?info` to show a URL's redirect URL instead of going there
 - use the API to generate short URLs:

   ```
   curl -X POST -d 'http://google.com' https://abbrv.de/
   https://abbrv.de/sdfasdfs
   curl -X POST -d '{"url": "https://ooogle.com", "expiry": "2016-10-14 13:30:00", "name": "myshortname"}'
   https://abbrv.de/myshortname
   ```
 - a simple config file for self hosting

## Features (tbd)

 - set an expiry time
 - a bookmarklet
 - optional support for login tokens/let only authenticated users a) see or b) create shortened URLs

## Non-Features (ntbd)

 - no tracking of clicks
 - no stats on anything
 - no plugins
