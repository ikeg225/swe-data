from trafilatura import fetch_url, extract, bare_extraction

class Posting:
    def __init__(self, url, position_title):
        self.posting = fetch_url(url)
        self.url = url
        self.position_title = position_title
        self.dict_posting = None
    
    def get_xml(self):
        return extract(self.posting, include_formatting=True, include_comments=False, include_links=True, output_format='xml')

    def get_dict(self):
        if not self.dict_posting:
            self.dict_posting = bare_extraction(self.posting)
        return self.dict_posting

    def get_position_title(self):
        return self.position_title
    
    def get_date(self):
        return self.get_dict()['date']

    #def get_position_title(self):
    #    words = self.get_dict()['title'].lower().split(" ")
    #    remove = {
    #        '-': None,
    #        '—': None,
    #        '–': None,
    #        'summer': None,
    #        'fall': None,
    #        'winter': None,
    #        'spring': None,
    #        ',': None,
    #        self.get_sitename().lower(): None
    #    }
    #    return [word.capitalize() for word in words if word not in remove].join(" ")
    
    def get_sitename(self):
        return self.get_dict()['sitename']

    def get_text(self):
        return self.get_dict()['text'].replace('\n', ' ')
        
    def get_url(self):
        return self.url
    
    def get_posting(self):
        return self.posting

#url = "https://akunacapital.com/job-details?gh_jid=4252792"

#post = Posting(url=url, position_title='full-stack engineer')