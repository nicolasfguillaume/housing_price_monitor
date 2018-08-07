# -*- coding: utf-8 -*-

HEADERS = {'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		  }

# if city == 'paris':
# 	FREQUENCY = 5 # min
# 	RATIO_MAX = 10000.0 # euros
# 	URLS = {'seloger': "https://www.seloger.com/list.htm?types=1%2C2&projects=2&sort=d_dt_crea&natures=1%2C2%2C4&price=150000%2F175000&surface=15%2FNaN&places=%5B%7Bcp%3A75%7D%5D&qsVersion=1.0&engine-version=new",
# 			'pap': "https://www.pap.fr/annonce/vente-appartement-maison-paris-75-g439-jusqu-a-175000-euros-a-partir-de-15-m2",
# 			'leboncoin': "https://www.leboncoin.fr/recherche/?category=9&region=12&departement=75&real_estate_type=2&price=min-175000"}

# if city == 'annemasse':
# 	FREQUENCY = 30 # min
# 	RATIO_MAX = 3500.0 # euros
# 	URLS = {'seloger': "https://www.seloger.com/list.htm?types=1%2C2&projects=2&sort=d_dt_crea&natures=1%2C2%2C4&price=50000%2F125000&surface=20%2FNaN&places=%5B%7Bci%3A740012%7D%5D&qsVersion=1.0",
# 			'pap': "https://www.pap.fr/annonce/vente-appartement-maison-annemasse-74100-g37475-entre-50000-et-125000-euros-a-partir-de-20-m2",
# 			'leboncoin': "https://www.leboncoin.fr/recherche/?category=9&cities=Annemasse_74100&real_estate_type=2&price=50000-125000&square=20-max"}

FREQUENCY = {'paris': 5, 'annemasse': 30} # min
RATIO_MAX = {'paris': 10000.0, 'annemasse': 3500.0}  # euros
URLS = {'paris': {'seloger': "https://www.seloger.com/list.htm?types=1%2C2&projects=2&sort=d_dt_crea&natures=1%2C2%2C4&price=150000%2F175000&surface=15%2FNaN&places=%5B%7Bcp%3A75%7D%5D&qsVersion=1.0&engine-version=new",
				  'pap': "https://www.pap.fr/annonce/vente-appartement-maison-paris-75-g439-jusqu-a-175000-euros-a-partir-de-15-m2",
				  'leboncoin': "https://www.leboncoin.fr/recherche/?category=9&region=12&departement=75&real_estate_type=2&price=min-175000"},

		'annemasse': {'seloger': "https://www.seloger.com/list.htm?types=1%2C2&projects=2&sort=d_dt_crea&natures=1%2C2%2C4&price=50000%2F125000&surface=20%2FNaN&places=%5B%7Bci%3A740012%7D%5D&qsVersion=1.0",
 					  'pap': "https://www.pap.fr/annonce/vente-appartement-maison-annemasse-74100-g37475-entre-50000-et-125000-euros-a-partir-de-20-m2",
 					  'leboncoin': "https://www.leboncoin.fr/recherche/?category=9&cities=Annemasse_74100&real_estate_type=2&price=50000-125000&square=20-max"}
}