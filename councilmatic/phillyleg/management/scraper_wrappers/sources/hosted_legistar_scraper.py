import datetime
import time
import httplib
import logging
import re
import urllib2
import utils
import urlparse
from collections import defaultdict

from legistar.scraper import LegistarScraper
from legistar.config import Config, DEFAULT_CONFIG

log = logging.getLogger(__name__)


class ScrapeError (Exception):
    pass


class HostedLegistarSiteWrapper (object):
    """
    A facade over the Philadelphia city council legistar site data.  It is
    responsible for scraping data out of the site.  The main external point
    of interaction is scrape_legis_file.

    requires: BeautifulSoup, mechanize
    """

    def __init__(self, **options):
        self.id_label = options.pop('id_label', 'Record #')
        self.url_label = options.pop('url_label', 'URL')
        self.type_label = options.pop('type_label', 'Type')
        self.status_label = options.pop('status_label', 'Status')
        self.title_label = options.pop('title_label', 'Title')
        self.intro_date_label = options.pop('intro_date_label', 'Intro Date')
        self.final_date_label = options.pop('final_date_label', 'Final Date')
        self.controlling_body_label = options.pop('controlling_body_label', 'Current Controlling Legislative Body')
        self.version_label = options.pop('version_label', 'Version')

        self.scraper = LegistarScraper(options)
        self.legislation_summaries =  self.scraper.searchLegislation('', created_before='2012-10-5')

    def scrape_legis_file(self, key, summary):
        '''Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL.'''

        while True :
            try:
                legislation_attrs, legislation_history = self.scraper.expandLegislationSummary(summary)
                break
            except urllib2.URLError as e:
                print e
                print 'skipping to next leg record'
            except AttributeError as e :
                print e
                print 'skipping to next leg record'
            while True :
                try:
                    summary = self.legislation_summaries.next()
                    break
                except urllib2.URLError as e:
                    print e
                    print 'sleeping for five minutes'
                    time.sleep('360')



            
        parsed_url = urlparse.urlparse(summary['URL'])
        key = urlparse.parse_qs(parsed_url.query)['ID'][0]
        
        # re-order the sponsor name by '[First] [Last]' instead of '[Last], [First]'
        sponsors = legislation_attrs['Sponsors']
        first_name_first_sponsors = []
        for sponsor in sponsors :
            if ',' in sponsor :
                name_list = sponsor.split(',')
                name_list.reverse()
                sponsor = ' '.join(name_list).strip()
            first_name_first_sponsors.append(sponsor)

        try:
            record = {
                'key' : key,
                'id' : summary[self.id_label],
                'url' : summary[self.url_label],
                'type' : summary[self.type_label],
                'status' : summary[self.status_label],
                'title' : summary[self.title_label],
                'controlling_body' : legislation_attrs[self.controlling_body_label],
                'intro_date' : self.convert_date(summary[self.intro_date_label]),
                'final_date' : self.convert_date(summary.setdefault(self.final_date_label, '')),
                'version' : summary.setdefault(self.version_label, ''),
                #'contact' : None,
                'sponsors' : first_name_first_sponsors,
                # probably remove this from the model as well
                'minutes_url'  : None
            }
        except KeyError, e:
            raise ScrapeError('Failed to find key %s in either summary keys '
                              '(%r) or attrs (%r)' % (e, summary.keys(), 
                                                    legislation_attrs.keys()))

        try:
            attachments = legislation_attrs['Attachments']
            for attachment in attachments:
                attachment['key'] = key
                attachment['file'] = attachment['label']
                attachment['description'] = attachment['label']
                del attachment['label']
        except KeyError:
            attachments = []

        actions = []
        for act in legislation_history :
            try:
                act_details, act_votes = self.scraper.expandHistorySummary(act)
            except (KeyError, AttributeError) as e:
                print e
                print summary
                continue
            try:
                acting_body = act['Action By']
                if not isinstance(acting_body, basestring):
                    acting_body = acting_body['label']

                action = {
                    'key' : key,
                    'date_taken' : self.convert_date(act['Date']),
                    'acting_body' : acting_body,
                    'motion' : act['Result'],
                    'description' : act['Action'],
                    'notes' : '',
                    'votes': [{'voter': vote['Person Name'],
                               'value': vote['Vote']}
                              for vote in act_votes]
                    }
            except TypeError as e:
                print e
                print summary
                continue
            except KeyError as e :
                print act
                print e
                print summary
                raise
            actions.append(action)

        # we should probably remove this from the model since the hosted
        # legistar does not have minutes
        minutes = []

        log.info('Scraped legfile with key %r' % (key,))
        log.debug("%r %r %r %r" % (record, attachments, actions, minutes))

        return record, attachments, actions, minutes

    def convert_date(self, orig_date):
        if orig_date:
            return datetime.datetime.strptime(orig_date, '%m/%d/%Y').date()
        else:
            return ''


    def check_for_new_content(self, last_key):
        '''Grab the next legislation summary row. Doesn't use the last_key
           parameter; just starts at the beginning for each instance of the
           scraper.
        '''
        try:
            print 'next leg record'
            next_summary = self.legislation_summaries.next()
            return 0, next_summary
        except StopIteration:
            return None, None

    def init_pdf_cache(self, pdf_mapping) :
        pass
        
    
