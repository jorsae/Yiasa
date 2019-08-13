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
                self.rules['Disallow'].append(disallow)
            elif line.startswith('allow'):
                allow = line.split(': ')[1].split(' ')[0]
                self.rules['Allow'].append(allow)