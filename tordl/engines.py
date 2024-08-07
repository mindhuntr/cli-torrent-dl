import json

from urllib.parse import urlencode

from bs4 import BeautifulSoup

from tordl.core import BaseDl, SearchResult


class KickAssTorrents(BaseDl):
    NAME = 'KAT'
    BASE_URL = 'https://kickasss.to'
    # BASE_URL = 'https://katcr.to'
    SEARCH_URL = '%s/search/%s/%s/' % (BASE_URL, '%s', '%s')

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (expression, str(self._current_index))

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        try:
            trs = bs.findAll('tr', class_='odd')
            trs.extend(bs.findAll('tr', class_='even'))
            for tr in trs:
                link = tr.find(class_='cellMainLink').attrs['href']
                size = tr.find(class_='nobr center').text.replace('\n', '')
                seeders = tr.find(class_='green center').text
                leechers = tr.find(class_='red lasttd center').text
                name = tr.find(class_='cellMainLink').text.replace('\n', ''). \
                    strip()
                result.append(
                    SearchResult(
                        self, name, link, seeders, leechers, size
                    )
                )
        except Exception:
            pass
        return result

    def _mk_magnet_url(self, link):
        return '%s%s' % (self.BASE_URL, link)

    def _process_magnet_link(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        try:
            m = bs.find('a', class_='kaGiantButton').attrs['href']
            return m
        except Exception:
            return None


class GloTorrents(BaseDl):
    NAME = 'Glo'
    BASE_URL = 'https://www.gtdb.to'
    SEARCH_URL = '%s/search_results.php?search=%s&sort=seeders&' \
                 'order=desc&page=%s' % (BASE_URL, '%s', '%s')

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (expression, str(self._current_index - 1))

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        try:
            trs = bs.find(class_='ttable_headinner').findAll('tr')[1:]
            for tr in trs:
                c2 = tr.findAll(class_='ttable_col2')
                if len(c2) > 1:
                    c1 = tr.findAll(class_='ttable_col1')
                    a = c2[0].findAll('a')[1]
                    name = a.attrs['title']
                    link = a.attrs['href']
                    magnet_url = c2[1].find('a').attrs['href']
                    size = c1[2].text
                    seeders = c2[2].find('b').text.replace(',', '')
                    leechers = c1[3].find('b').text.replace(',', '')
                    result.append(
                        SearchResult(
                            self,
                            name,
                            link,
                            seeders,
                            leechers,
                            size,
                            magnet_url
                        )
                    )
        except Exception:
            pass
        return result

    def _mk_magnet_url(self, link):
        pass

    def _process_magnet_link(self, response):
        pass


class TpbParty(BaseDl):
    NAME = 'TPB'
    BASE_URL = 'https://tpb.party'
    SEARCH_URL = '%s/search/%s/%s/99/0' % (BASE_URL, '%s', '%s')

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (expression, str(self._current_index))

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        try:
            trs = bs.find('table', id='searchResult').findAll('tr')[1:]
            for tr in trs:
                a = tr.find(class_='detName').find('a')
                name = a.text
                link = '/%s' % '/'.join(a.attrs['href'].split('/')[3:])
                tds = tr.findAll('td')
                magnet_url = tds[1].findAll('a')[1].attrs['href']
                seeders = tds[2].text
                leeches = tds[3].text
                size = tr.find(class_='detDesc').text.split(',')[1]
                size = size.replace('Size ', '').replace('i', '')
                result.append(
                    SearchResult(
                        self,
                        name,
                        link,
                        seeders,
                        leeches,
                        size,
                        magnet_url
                    )
                )
        except Exception:
            pass

        return result

    def _mk_magnet_url(self, link):
        pass

    def _process_magnet_link(self, response):
        pass


class LimeTorrents(BaseDl):
    NAME = 'Lime'
    BASE_URL = 'https://www.limetorrents.lol'
    SEARCH_URL = '%s/search/all/%s/seeds/%s/' % (BASE_URL, '%s', '%s')

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (expression, str(self._current_index))

    def _mk_magnet_url(self, link):
        return '%s%s' % (self.BASE_URL, link)

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        trs = bs.findAll('tr', attrs={'bgcolor': '#F4F4F4'})
        trs.extend(bs.findAll('tr', attrs={'bgcolor': '#FFFFFF'}))
        for tr in trs:
            try:
                a = tr.find(class_='tt-name').findAll('a')[1]
                name = a.string
                link = a.attrs['href']
                size = tr.findAll(class_='tdnormal')[1].string
                seeders = tr.find(class_='tdseed').string.replace(',', '')
                leechers = tr.find(class_='tdleech').string.replace(',', '')
                result.append(
                    SearchResult(
                        self, name, link, seeders, leechers, size
                    )
                )
            except Exception:
                pass

        return result

    def _process_magnet_link(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        try:
            return bs.findAll(class_='csprite_dltorrent')[2].attrs['href']
        except Exception:
            pass

        return None


class Dl1337xto(BaseDl):
    NAME = '1337x'
    BASE_URL = 'https://1337x.to'
    SEARCH_URL = '%s/search/%s/%s/' % (BASE_URL, '%s', '%s')

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (expression, str(self._current_index))

    def _mk_magnet_url(self, magnet_page_link):
        return '%s%s' % (self.BASE_URL, magnet_page_link)

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        try:
            trs = bs.find(
                class_='table-list table table-responsive table-striped'
            ).find('tbody').findAll('tr')
            for tr in trs:
                tds = tr.findAll('td')

                a = tds[0].findAll('a')[1]
                name = a.string
                link = a.attrs['href']

                seeders = tds[1].string
                leechers = tds[2].string
                size = '%sB' % tds[4].text.split('B')[0]

                result.append(
                    SearchResult(
                        self, name, link, seeders, leechers, size
                    )
                )
        except Exception:
            pass

        return result

    def _process_magnet_link(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        try:
            x = bs.find(class_='box-info torrent-detail-page')
            if not x:
                x = bs.find(
                    class_=
                    'box-info torrent-detail-page series-torrent vpn-info-wrap'
                )
            x = x.findAll('div')[1].find('div').find('ul').find('li').find('a')
            return x.attrs['href']
        except Exception:
            return None


class NyaaTracker(BaseDl):
    NAME = 'Nyaa'
    BASE_URL = 'https://nyaa.si'
    SEARCH_URL = '%s/?f=0&c=0_0&q=%s&p=%s&s=seeders&o=desc' % (
        BASE_URL, '%s', '%s'
    )

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (
            expression, str(self._current_index)
        )

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        try:
            trs = bs.find('tbody').findAll('tr')
            for tr in trs:
                tds = tr.findAll('td')[1:]
                # Remove link to comments that some listings have.
                # Most concise way I have found so far.
                for a in tds[0].findAll(class_='comments'):
                    a.decompose()
                a = tds[0].find('a')
                name = a.attrs['title']
                link = a.attrs['href']
                magnet_url = tds[1].findAll('a')[1].attrs['href']
                # Site uses binary prefixes.
                # Should calculate proper sizes at some point.
                size = tds[2].text.replace('i', '')
                seeders = tds[4].text
                leechers = tds[5].text
                result.append(
                    SearchResult(
                        self,
                        name,
                        link,
                        seeders,
                        leechers,
                        size,
                        magnet_url
                    )
                )
        except Exception:
            pass

        return result

    def _mk_magnet_url(self, link):
        pass

    def _process_magnet_link(self, response):
        pass


class SukebeiNyaa(NyaaTracker):
    NAME = 'Sukebei'
    BASE_URL = 'https://sukebei.nyaa.si'
    SEARCH_URL = '%s/?f=0&c=0_0&q=%s&p=%s&s=seeders&o=desc' % (
        BASE_URL, '%s', '%s'
    )


class TorrentGalaxy(BaseDl):
    NAME = 'TGx'
    BASE_URL = 'https://torrentgalaxy.to'
    SEARCH_URL = '%s/torrents.php?search=%s&sort=seeders&order=desc&page=%s' % (
        BASE_URL, '%s', '%s'
    )

    def _mk_search_url(self, expression):
        return self.SEARCH_URL % (
            expression, str(self._current_index)
        )

    def _process_search(self, response):
        bs = BeautifulSoup(response, features='html.parser')
        result = []
        try:
            rows = bs.findAll('div', class_='tgxtablerow')
            for r in rows:
                cells = r.findAll('div', class_='tgxtablecell')[3:]
                a = cells[0].find('a')
                name = a.attrs['title']
                link = a.attrs['href']
                magnet_url = cells[1].findAll('a')[1].attrs['href']
                size = cells[4].find('span').text
                bs = cells[7].findAll('b')
                seeders = bs[0].text
                leechers = bs[1].text
                result.append(
                    SearchResult(
                        self,
                        name,
                        link,
                        seeders,
                        leechers,
                        size,
                        magnet_url
                    )
                )
        except Exception:
            pass

        return result

    def _mk_magnet_url(self, link):
        pass

    def _process_magnet_link(self, response):
        pass
