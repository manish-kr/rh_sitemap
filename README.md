# Redhat Sitemap Generator

This scrapy module crawls all available sites on ```https://redhat.com``` or any given website and it extracts all URLs. Using the URLs a sitemap is generated.
according to the protocol described at http://www.sitemaps.org/protocol.html.

## Installation

You can use pip to install the required dependencies. The requirements.txt file contains list of all dependencies.

```NOTE: On a windows machines you will need to install an additional  package pywin32, which is also included in requirements.txt. It won't be needed while running this script on windows.```

    $ pip install -r requirements.txt

When using pip it's maybe necessary to install some development packages.
For example on Ubuntu 16.04 install the following packages.

    $ sudo apt install gcc libssl-dev python-dev python-virtualenv

## Usage

To generate a new sitemap file simply run the spider using the
following command.The result will be available in the file ```sitemap_redhat.openstack.org.xml```.

    $ scrapy crawl rhsitemap

It might take several minutes to hours, to crawl all available sites on https://redhat.com. So it's suggested to set the attribute ```DEPTH_LIMIT``` which triggering the execution.

    $ scrapy crawl rhsitemap -s DEPTH_LIMIT=3
    
It's also possible to crawl other sites using the attribute ```domain```.

For example to crawl http://developer.redhat.com use the following command.

    $ scrapy crawl rhsitemap -a domain=developer.redhat.com

To write log messages into a file append the parameter ```-s LOG_FILE=scrapy.log```.

To view the HTML report, just open the generate file with any browser. If the file size is big, it might take longer than usual to load the page.
