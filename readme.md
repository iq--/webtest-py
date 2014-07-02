# Overview

Check web page status with webtest.py.

# Usage

`python ./webtest.py PATH_TO_CONFIG` for example:

    python ./webtest.py ./webtest.example.conf

# Config syntax

Each line is a test or comment. Format: `HTTP_CODE URL #comment`. For example:

    # Good urls
    200 https://www.python.org/
    301 https://www.python.org/about           # redirect to about/
    200 https://www.python.org/about/
    404 https://www.python.org/iq--
    
    # Bad urls
    200 https://www.python.org/iq--

