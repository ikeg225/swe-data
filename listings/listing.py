import re
import requests
from proxy import Proxy
from locations import places, english
from bs4 import BeautifulSoup
from useragent import UserAgent

class Listing:
    def __init__(self, url, db, proxyOn=True, headers=None):
        self.proxyOn = proxyOn
        self.url = url
        self.headers = headers
        self.db = db

        if proxyOn:
            proxy = Proxy()
            self.proxies = {
                'http': 'http://' + proxy.getProxy(),
                'https': 'http://' + proxy.getProxy(),
            }
        success = False
        
        while success != True:
            try:
                self.req = self.get_req(url, headers, redirect=False)
                self.req.raise_for_status()
                self.posting = BeautifulSoup(self.req.content, 'lxml')
                self.baseurl = re.match('^https?:\/\/[^#?\/]+', url)[0]
                success = True
            except Exception as err:
                print(err)
    
    @staticmethod
    def clean_string(string):
        return re.sub('[\W]+', '', string).lower()
    
    @staticmethod
    def clean_title(title):
        time = set(['summer', 'fall', 'winter', 'spring'])
        upper = set(['ios', 'ui', 'it', 'ai', 'ml', 'qa', 'co', 'op', 'nx', 'sql', 'ee', 'cpu', 'go', 'dbs', 'aws', 'swe', 'api', 'gpu', 'sde', 'usb', 'os', 'ip', 'nlp'])
        co, op = False, False
        new_title, locations, times = [], [], []
        for word in title:
            if word in time or word.isnumeric() or word in places or word in english:
                if word in places or word in english:
                    locations.append(word.capitalize())
                else:
                    times.append(word.capitalize())
                if word == 'co':
                    co = True
                if word == "op":
                    op = True
            else:
                if word in upper:
                    new_title.append(word.upper())
                else:
                    new_title.append(word.capitalize())
        if co and op:
            new_title.append("CO-OP")
        return { "position": ' '.join(new_title), "locations": ','.join(locations), "times": ' '.join(times) }
    
    @staticmethod
    def swe_position(title):
        intern_check, field_check = False, False
        intern_keywords = set(['intern', 'internship', 'co', 'op', 'co-op', 'apprenticeship', 'apprentice', 'student', 'undergrad'])
        field_keywords = set(['pipeline', 'server', 'connectivity', 'tableau', 'ethernet', 'artificial', 'c', 'dev', 'proxies', 'game', 
        'connection', 'programmer', 'implementation', 'financial', 'data', 'ee', 'request', 'computational', 'modeler', 'interfaces', 'information', 
        'platform', 'ruby', 'ciso', 'tools', 'analytic', 'test', 'raspberry', 'architect', 'python', 'energy', 'ios', 'qa', 'hardware', 'processor', 
        'programs', 'software', 'textract', 'cpu', 'signal', 'app', 'code', 'autodesk', 'sql', 'technologies', 'exploratory', 'golang', 'systems', 'solutions', 
        'cyberpatriot', 'developer', 'technicien', 'packages', 'web', 'processing', 'aerospace', 'dbs', 'socket', 'electronic', 'detect', 'security', 'cyber', 
        'embedded', 'computing', 'circularity', 'giscience', 'engine', 'infrastructure', 'auto', 'requests', 'aws', 'programme', 'proxy', 'analyst', 'swe', 'back', 
        'algorithms', 'backend', 'probabilistic', 'operation', 'development', 'android', 'integration', 'compiler', 'json', 'dell', 'debug', 'tech', 'detection', 
        'ml', 'engineering', 'machine', 'react', 'autonomous', 'spatial', 'validation', 'c#', 'http', 'quantitative', 'complier', 'sw', 'emulation', 'infosec', 
        'sensors', 'assurance', 'modeling', 'frontend', 'r', 'tool', 'technology', 'technician', 'computer', 'api', 'gpu', 'support', 'programming', 'automated', 
        'usb', 'front', 'algorithm', 'sde', 'devops', 'urlopen', 'deep', 'neuromotor', 'core', 'engineer', 'process', 'devices', 'device', 'technican', 
        'driver', 'documentation', 'interface', 'end', 'java', 'intel', 'wireless', 'swift', 'ops', 'internal', 'risk', 'system', 'strategy', 'optimization', 'analysis', 
        'integrity', 'innovation', 'sourcing', 'mobile', 'prediction', 'automations', 'urllib', 'reliability', 'cloud', 'prisma', 'robotic', 'electrical', 'adapters', 
        'framework', 'frameworks', 'ai', 'forecasting', 'os', 'graphs', 'full', 'spark', 'circuits', 'polytechnic', 'compute', 'quality', 'devop', 'c++', 'trading', 'quantum', 
        'applied', 'graphics', 'simulation', 'operations', 'reinforcement', 'architecture', 'typescript', 'silicon', 'firmware', 'testing', 'stack', 'operating', 'robotics', 
        'natural', 'production', 'go', 'applications', 'recognition', 'windows', 'trade', 'performance', 'vmware', 'predictive', 'angular', 'automation', 'virtual', 'site', 
        'application', 'monitoring', 'javascript', 'user', 'opertions', 'it', 'cybersecurity', 'ip', 'technical', 'sensor', 'power', 'network', 'solution', 'datapath', 'gaming', 
        'mechanical', 'nlp', 'analytics', 'module', 'coding', 'models', 'chipsets'])
        for word in title:
            if word in field_keywords:
                field_check = True
            elif word in intern_keywords:
                intern_check = True
            if intern_check and field_check:
                return True
        return False

    def get_listing(self):
        urls = set()
        for url in self.posting.find_all('a', href=True):
            title = url.get_text().strip().lower().replace("\n", " ")
            filtered = list(filter(None, re.split('(?![\+\#])[\W]', title)))
            if Listing.swe_position(filtered):
                position = Listing.clean_title(filtered)
                urls.add((self.add_base_url(url.get('href')), position["position"], position["locations"], position["times"]))
        return urls
    
    def add_base_url(self, slug):
        if not self.baseurl in slug:
            slug = self.baseurl + slug
        return slug
    
    def get_posting(self):
        return self.posting
    
    def get_raw(self):
        return self.req.content

    def get_req(self, url, headers, redirect=True):
        if self.proxyOn:
            headers = {
                'user-agent': UserAgent.randomAgent()
            }
            return requests.get(url, proxies=self.proxies, headers=headers, allow_redirects=redirect)
        else:
            return requests.get(url, headers=headers, allow_redirects=redirect)
    
    def add_to_database(self, id, company, company_short, main_url, name, post_url, locations, date, timeframe, contents, currentday, posted, posted_num, payhour):
        self.db.collections['postings'].documents.upsert({
            'id': id,
            'company': company,
            'companyShort': company_short,
            'mainURL': main_url,
            'name': name, 
            'postURL': post_url, 
            'locations': locations, 
            'date': date, 
            'timeframe': timeframe,
            'contents': contents,
            'currentday': currentday,
            'posted': posted,
            'postedNum': posted_num,
            'payhour': payhour
        })
        print(id)
        return
    
    def get_favicon(self, name, url):
        favicon = "https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://" + url + "&size=256"
        try:
            response = self.get_req(favicon, self.headers, redirect=False)
            response.raise_for_status()
            with open("../swe/images/logos/" + name + ".png", 'wb') as f:
                f.write(response.content)
            return True
        except Exception as err:
            print(err)
            return False
    
    def add_company(self, company, company_short, main_url):
        search_parameters = {
            'q'         : '*',
            'query_by'  : 'company',
            'filter_by' : 'id:=' + company_short
        }
        
        if self.db.collections['companies'].documents.search(search_parameters)["found"] == 0:
            found_logo = self.get_favicon(name=company_short, url=main_url)
            document = {
                'id': company_short,
                'company': company,
                'mainURL': main_url,
                'foundLogo': found_logo
            }
            self.db.collections['companies'].documents.create(document)
        
        print(company_short)
        return