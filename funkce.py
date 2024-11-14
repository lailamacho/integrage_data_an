def name_to_col(name: str) -> str:
    """
    Ze zadaného názvu sub_tématu vrací název sloupce v csv exportu.
    """
    dovednosti_sub_topics = {"sub_topic_3": "Odborné dovednosti a jejich rozvoj",
                "sub_topic_4": "Flexibilita",
                "sub_topic_5": "Zdravotní stav",
                "sub_topic_6": "Sebedůvěra a motivace",
                "sub_topic_7": "Finanční a sociální bariéry"}
    
    os_rozvoj_sub_topics = {"sub_topic_8": "Životní spokojenost",
                            "sub_topic_12": "Pracovní spokojenost",
                            "sub_topic_19": "Pracovní benefity",
                            "sub_topic_20": "Problémy na pracovišti"}

    tech_zdatnost_sub_topics = {"sub_topic_13": "Základní počítačové dovednosti",
                                "sub_topic_14": "Práce s kancelářským softwarem",
                                "sub_topic_15": "Internetové dovednosti",
                                "sub_topic_16": "Komunikace a sociální sítě",
                                "sub_topic_17": "Řešení problémů a správa systému",
                                "sub_topic_18": "Produktivita a digitální tvorba"}
    
    dict_list = [dovednosti_sub_topics, os_rozvoj_sub_topics, tech_zdatnost_sub_topics]

    for x in dict_list:
        for i in x:
            if x[i] == name:
                return i


def col_to_name(col: str) -> str:
    """
    Z názvu sloupce v csv ecportu vrací název odpovídajícího sub_tématu.
    """
    dovednosti_sub_topics = {"sub_topic_3": "Odborné dovednosti a jejich rozvoj",
                "sub_topic_4": "Flexibilita",
                "sub_topic_5": "Zdravotní stav",
                "sub_topic_6": "Sebedůvěra a motivace",
                "sub_topic_7": "Finanční a sociální bariéry"}
    
    os_rozvoj_sub_topics = {"sub_topic_8": "Životní spokojenost",
                            "sub_topic_12": "Pracovní spokojenost",
                            "sub_topic_19": "Pracovní benefity",
                            "sub_topic_20": "Problémy na pracovišti"}

    tech_zdatnost_sub_topics = {"sub_topic_13": "Základní počítačové dovednosti",
                                "sub_topic_14": "Práce s kancelářským softwarem",
                                "sub_topic_15": "Internetové dovednosti",
                                "sub_topic_16": "Komunikace a sociální sítě",
                                "sub_topic_17": "Řešení problémů a správa systému",
                                "sub_topic_18": "Produktivita a digitální tvorba"}

    dict_list = [dovednosti_sub_topics, os_rozvoj_sub_topics, tech_zdatnost_sub_topics]

    for x in dict_list:
        if col in x.keys():
            return x.get(col)


def col_to_topic(col: str) -> str:
    """
    Pro zadaný název sloupce v csv exportu vrací název příslušné kompetence (název dotazníku).
    """
    dovednosti_sub_topics = {"sub_topic_3": "Odborné dovednosti a jejich rozvoj",
                "sub_topic_4": "Flexibilita",
                "sub_topic_5": "Zdravotní stav",
                "sub_topic_6": "Sebedůvěra a motivace",
                "sub_topic_7": "Finanční a sociální bariéry"}
    
    os_rozvoj_sub_topics = {"sub_topic_8": "Životní spokojenost",
                            "sub_topic_12": "Pracovní spokojenost",
                            "sub_topic_19": "Pracovní benefity",
                            "sub_topic_20": "Problémy na pracovišti"}

    tech_zdatnost_sub_topics = {"sub_topic_13": "Základní počítačové dovednosti",
                                "sub_topic_14": "Práce s kancelářským softwarem",
                                "sub_topic_15": "Internetové dovednosti",
                                "sub_topic_16": "Komunikace a sociální sítě",
                                "sub_topic_17": "Řešení problémů a správa systému",
                                "sub_topic_18": "Produktivita a digitální tvorba"}

    dict_dict = {"Dovednosti pro začlenění na pracovišti": dovednosti_sub_topics,
                 "Osobní rozvoj a blahobyt": os_rozvoj_sub_topics,
                 "Technologická zdatnost": tech_zdatnost_sub_topics}

    for name, values in dict_dict.items():
        if col in values:
            return name


def my_dicts(choice) -> dict:
    assert choice in ["D", "O", "T"], "Povolené hodnoty parametru = D, O, T"

    dovednosti_sub_topics = {"sub_topic_3": "Odborné dovednosti a jejich rozvoj",
                "sub_topic_4": "Flexibilita",
                "sub_topic_5": "Zdravotní stav",
                "sub_topic_6": "Sebedůvěra a motivace",
                "sub_topic_7": "Finanční a sociální bariéry"}
    
    os_rozvoj_sub_topics = {"sub_topic_8": "Životní spokojenost",
                            "sub_topic_12": "Pracovní spokojenost",
                            "sub_topic_19": "Pracovní benefity",
                            "sub_topic_20": "Problémy na pracovišti"}

    tech_zdatnost_sub_topics = {"sub_topic_13": "Základní počítačové dovednosti",
                                "sub_topic_14": "Práce s kancelářským softwarem",
                                "sub_topic_15": "Internetové dovednosti",
                                "sub_topic_16": "Komunikace a sociální sítě",
                                "sub_topic_17": "Řešení problémů a správa systému",
                                "sub_topic_18": "Produktivita a digitální tvorba"}
    
    if choice == "D":
        return dovednosti_sub_topics
    elif choice == "O":
        return os_rozvoj_sub_topics
    elif choice == "T":
        return tech_zdatnost_sub_topics
    


country_code = {
       "AL": ["Albánie", "Albania"],
       "AD": ["Andorra", "Andorra"],
       "AT": ["Rakousko", "Austria"],
       "BY": ["Bělorusko", "Belarus"],
       "BE": ["Belgie", "Belgium"],
       "BA": ["Bosna a Hercogovina", "Bosnia and Herzegovina"],
       "BG": ["Bulharsko", "Bulgaria"],
       "HR": ["Chorvatko", "Croatia"],
       "CY": ["Kypr", "Cyprus"],
       "CZ": ["Česká republika", "Czech Republic (Czechia)"],
       "DK": ["Dánsko", "Denmark"],
       "EE": ["Estónsko", "Estonia"],
       "FI": ["Finsko", "Finland"],
       "FR": ["Francie", "France"],
       "GE": ["Gruzie", "Georgia"],
       "DE": ["Německo", "Germany"],
       "GR": ["Řecko", "Greece"],
       "HU": ["Maďarsko", "Hungary"],
       "IS": ["Island", "Iceland"],
       "IE": ["Irsko", "Ireland"],
       "IT": ["Itálie", "Italy"],
       "XK": ["Kosovo", "Kosovo"],
       "LV": ["Lotyšško", "Latvia"],
       "LI": ["Lichtenštejnsko", "Liechtenstein"],
       "LT": ["Litva", "Lithuania"],
       "LU": ["Lucembursko", "Luxembourg"],
       "MT": ["Malta", "Malta"],
       "MD": ["Moldavsko", "Moldova"],
       "MC": ["Monako", "Monaco"],
       "ME": ["Černá hora", "Montenegro"],
       "NL": ["Nizozemsko", "Netherlands"],
       "MK": ["Severní Makedonie", "North Macedonia (FYROM)"],
       "NO": ["Norsko", "Norway"],
       "PL": ["Polsko", "Poland"],
       "PT": ["Portugalsko", "Portugal"],
       "RO": ["Rumunsko", "Romania"],
       "RU": ["Rusko", "Russia"],
       "SM": ["San Marino", "San Marino"],
       "RS": ["Srbsko", "Serbia"],
       "SK": ["Slovensko", "Slovakia"],
       "SI": ["Slovinsko", "Slovenia"],
       "ES": ["Španělsko", "Spain"],
       "SE": ["Švédsko", "Sweden"],
       "CH": ["Švýcarsko", "Switzerland"],
       "UA": ["Ukrajina", "Ukraine"],
       "GB": ["Velká Británie", "United Kingdom"],
       "VA": ["Vatikán", "Vatican City (Holy See)"]
   }