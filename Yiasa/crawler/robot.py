import re

class Robots:
    def __init__(self):
        self.rules = {'Allow':[], 'Disallow':[]}
    
    def parse_robots(self, text):
        user_agent = True
        for line in text.lower().split('\n'):
            if line.startswith('user-agent'):
                if '*' in line:
                    user_agent = True
                else:
                    user_agent = False
            
            if user_agent is False:
                continue

            if line.startswith('disallow'):
                disallow = line.split(': ')[1].split(' ')[0]
                self.rules['Disallow'].append(self.clean_regex(disallow))
            elif line.startswith('allow'):
                allow = line.split(': ')[1].split(' ')[0]
                self.rules['Allow'].append(self.clean_regex(allow))
    
    def clean_regex(self, rule):
        rule = rule.replace('.', '\.')
        rule = rule.replace('^', '\^')
        rule = rule.replace('$', '\$')
        rule = rule.replace('+', '\+')
        rule = rule.replace('?', '\?')
        rule = rule.replace('*', '\S+')
        return rule

    def can_crawl_url(self, url):
        for disallow in self.rules['Disallow']:
            if re.search(disallow, url, re.IGNORECASE):
                return False
        return True
    
    def __str__(self):
        return f'Allow: {self.rules["Allow"]}\nDisallow: {self.rules["Disallow"]}'