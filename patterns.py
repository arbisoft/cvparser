section_patterns = [
    {"label":"SECTIONS", "pattern":[{"lower":"career"},{"lower":"objective"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"work"},{"lower":"experience"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"work"},{"lower":"history"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"work"},{"lower":"experience"},{"lower":"summary"},{"TEXT":":"}]},
    {"label":"SECTIONS", "pattern":[{"lower":"education"},{"TEXT":":"}]},
    {"label": "SECTIONS", "pattern":[{"lower":"strengths"},{'TEXT':{'REGEX':'\n'}}]},
    {"label": "SECTIONS", "pattern":[{"lower":"education"},{'TEXT':{'REGEX':'\n'}}]},
    {"label": "SECTIONS", "pattern":[{"lower":"experience"},{'TEXT':{'REGEX':'\n'}}]},
    {"label": "SECTIONS", "pattern":[{"lower":"skills"},{'TEXT':{'REGEX':'\n'}}]},
    {"label": "SECTIONS", "pattern":[{"lower":"projects"},{'TEXT':{'REGEX':'\n'}}]},
    {"label": "SECTIONS", "pattern":[{"lower":"interest"},{'TEXT':{'REGEX':'\n'}}]},

    {"label": "SECTIONS", "pattern":[{"lower":"summary"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"technical"},{"lower":"skills"},{"TEXT":":"}]},
    {"label":"SECTIONS", "pattern":[{"lower":"professional"},{"lower":"summary"},{"TEXT":":"}]},
    {"label":"SECTIONS", "pattern":[{"lower":"professional"},{"lower":"development"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"projects"},{"lower":"information"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"educational"},{"lower":"background"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"academic"},{"lower":"projects"},{'TEXT':{'REGEX':'\n'}}]},


    {"label":"SECTIONS", "pattern":[{"lower":"roles"},{"lower":"&"},{"lower":"responsibilities"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"career"},{"lower":"objective"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"technical"},{"lower":"profile"},{'TEXT':{'REGEX':'\n'}}]},
    {"label":"SECTIONS", "pattern":[{"lower":"professional"},{"lower":"skills"},{'TEXT':{'REGEX':'\n'}}]}, 
    {"label": "SECTIONS", "pattern":[{"lower":"w"},{"lower":"o"},{"lower":"r"},{"lower":"k"},{"is_space":True},{"lower":"e"},{"lower":"x"},{"lower":"p"},{"lower":"e"},{"lower":"r"},{"lower":"i"},{"lower":"e"},{"lower":"n"},{"lower":"c"},{"lower":"e"}]},
    {"label": "SECTIONS", "pattern":[{"lower":"e"},{"lower":"d"},{"lower":"u"},{"lower":"c"},{"lower":"a"},{"lower":"t"},{"lower":"i"},{"lower":"o"},{"lower":"n"}]},
    {"label": "SECTIONS", "pattern":[{"lower":"r"},{"lower":"e"},{"lower":"f"},{"lower":"e"},{"lower":"r"},{"lower":"e"},{"lower":"n"},{"lower":"c"},{"lower":"e"},{"lower":"s"}]},
    {"label": "SECTIONS", "pattern":[{"lower":"s"},{"lower":"k"},{"lower":"i"},{"lower":"l"},{"lower":"l"},{"lower":"s"}]},
    {"label": "SECTIONS", "pattern":[{"lower":"a"},{"lower":"b"},{"lower":"o"},{"lower":"u"},{"lower":"t"},{"is_space":True},{"lower":"m"},{"lower":"e"}]},
]


patterns = [ 
    
    #patterns for ID Card
    {"label":"NIC", "pattern":[{"LIKE_NUM":True,"length":5},{"TEXT":{"REGEX":"[–-]"}},{"LIKE_NUM":True,"length":7} ,{"TEXT":{"REGEX":"[–-]"}},{"LIKE_NUM":True,"length":1}]},
    {"label":"NIC", "pattern":[{"LIKE_NUM":True,"length":14}]},


    #patterns for email
    {"label":"EMAIL","pattern":[{"LIKE_EMAIL":True}]},

    #patterns for cellphone
    {"label":"CELL", "pattern":[{"LIKE_NUM":True,"length":3},{"IS_PUNCT": True},{"LIKE_NUM":True,"length":3},{"IS_PUNCT": True},{"LIKE_NUM":True,"length":7}]},
    {"label":"CELL", "pattern":[{"LIKE_NUM":True,"length":3},{"LIKE_NUM":True,"length":3},{"LIKE_NUM":True,"length":7}]},
    {"label":"CELL", "pattern":[{"LIKE_NUM":True,"length":4},{"TEXT":{"REGEX":"[–-]"}},{"LIKE_NUM":True,"length":7}]},
    #{"label":"CELL", "pattern":[{"TEXT":{"REGEX":"\+\d+.\d+.\d+"}}]},
    {"label":"CELL", "pattern":[{"TEXT":'('},{'like_num':True},{"TEXT":')'},{'like_num':True,'length':7}]},
    {"label": "LINKS", "pattern":[{"LIKE_URL":True}]},

    #patterns for skills
    {"label":"SKILL", "pattern":[{"lower":"c#.net"}]},
    {"label":"SKILL", "pattern":[{"lower":"java"}]},
    {"label":"SKILL", "pattern":[{"lower":"c++"}]},
    {"label":"SKILL", "pattern":[{"lower":"asp.net"}]},
    {"label":"SKILL", "pattern":[{"lower":"ms"},
                                {"is_punct":True},
                                {"lower":"access"}]},
    {"label":"SKILL", "pattern":[{"lower":"ms"},{"is_punct":True},{"lower":"office"}]},
    {"label":"SKILL", "pattern":[{"lower":"ms"},{"is_punct":True},{"lower":"sql"}]},
    {"label":"SKILL", "pattern":[{"lower":"c++"}]},
    {"label":"SKILL", "pattern":[{"lower":"unity3d"}]},
    {"label":"SKILL", "pattern":[{"lower":"matlab"}]},
    {"label":"SKILL", "pattern":[{"lower":"c#"}]},
    {"label":"SKILL", "pattern":[{"lower":"html"}]},
    {"label":"SKILL", "pattern":[{"lower":"javascript"}]},
    {"label":"SKILL", "pattern":[{"lower":"reactjs"}]},
    {"label":"SKILL", "pattern":[{"lower":"css"}]},
    {"label":"SKILL", "pattern":[{"lower":"php"}]},
    {"label":"SKILL", "pattern":[{"lower":"wordpress"}]},
    {"label":"SKILL", "pattern":[{"lower":"jquery"}]},
    {"label":"SKILL", "pattern":[{"lower":"bootstrap"}]},
    {"label":"SKILL", "pattern":[{"lower":"reactjs"}]},
    {"label":"SKILL", "pattern":[{"lower":"swift"}]},
    {"label":"SKILL", "pattern":[{"lower":"ios"}]},
    {"label":"SKILL", "pattern":[{"lower":"xcode"}]},
    {"label":"SKILL", "pattern":[{"lower":"objective"},{"is_punct":True},{"lower":"c"}]},
    
]