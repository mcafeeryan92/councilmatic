Local Instance of Councilmatic
==============================

Setting up the server
---------------------

	virtualenv env
	source env/bin/activate
	pip install -r requirements.txt
	cp local_settings.py.template local_settings.py

Create a PostGIS database called 'councilmatic'. Refer to the [GeoDjango documentation](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/) or other PostGIS documentation for instructions.

	python website/manage.py syncdb
	python website/manage.py migrate

If you chose to create a superuser during the `syncdb` command, you should now create a subscriber for that superuser. A subscriber could not be created until the subscriptions app's database tables were set up, and that didn't happen until the `migrate` command. Now that the subscription app is ready, sync the subscriber objects:

	python website/manage.py syncsubscribers

Now you should be able to run the site:

	python website/manage.py runserver


Loading Data
------------

Councilmatic works right now with locally-hosted and Granicus-hostes versions of the legislative management software called [Legistar](http://www.granicus.com/Legistar/Product-Overview.aspx). For a partial list of hosted Legistar instances, see [this list](https://docs.google.com/spreadsheet/ccc?key=0Aqm9N7Oy6TlzdGhsLWlHMDNoZFZRSDZpZ1JEWk5LVmc#gid=0).

Right now, The [Legistar scraper](https://github.com/fgregg/legistar-scrape) that Councilmatic uses is known to work for [Philadelphia](http://philly.councilmatic.org/) and [Chicago](http://chicagolegistar.org/). You may need to make some tweaks in order to get it to work with your city's Legistar. If you need help, try hanging out in the #councilmatic channel on Freenode IRC.

To configure the scraper to load data for your city, open local_settings.py. Uncomment the legislation settings section that is appropriate for your city's source of legislation. These settings look like:

	LEGISLATION = {
		...
	}

### Settings

* 'SYSTEM'

  If your city uses a self-hosted version of Legistar (the host name doesn't end in legistar.com), it's probably a self-hosted version of Legistar. In this case, set the `'SYSTEM'` attribute to `'Daystar Insite'`. If it is a hosted version of Legistar, set the attribute to `'Granicus Legistar'`.

* 'ROOT'

  The root address of your city's legistar server. For example: `'http://phila.legistar.com/'`.

* 'ADDRESS_BOUNDS'
  
  A bounding box to give the geocoder a hint as to where addresses it finds should be located. This should be a list with four values, [lat1, lng1, lat2, lng2].

* 'ADDRESS_SUFFIX'

  A string to be tacked on to the end of addresses to help the geocoder identify places. For example, `', Philadelphia, PA'` ('701 Chestnut' would become '701 Chestnut, Philadelphia, PA').

* 'SCRAPER'

  The site scraper class to use. For the hosted Legistar, this will be:

  `'phillyleg.management.scraper_wrappers.sources.hosted_legistar_scraper.HostedLegistarSiteWrapper'`

* 'SCRAPER_OPTIONS'
  
  These will be passed in as keyword options to the `SCRAPER` class during construction.


### Importing

To actually import data from the legislation source, run the following:

	python website/manage.py updatelegsfiles  # Load the legislation
	python website/manage.py update_index  # Update the search indexes

Let the `updatelegfiles` command run for a couple of minutes, just to get some data to work with. 