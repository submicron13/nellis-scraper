class Items:
    def __init__(self):
        self._items = []

    def add_item(self, search,  item):
        
        self._items.append({"search": search, "item": item})
    
    @property
    def items(self):
        return self._items

class Item:
    def __init__(self, title, retail, location, price, bid, time_left, url, img_url):
        self._title = title
        self._retail = retail
        self._location = location
        self._price = price
        self._bid = bid
        self._time_left = time_left
        self._url = url
        self._img_url = img_url 
    
    def __str__(self):
        return f"Title: {self._title}"
    @property    
    def title(self):
        return self._title
    @property    
    def retail(self):
        return self._retail
    @property    
    def location(self):
        return self._location
    @property    
    def price(self):
        return self._price
    @property    
    def bid(self):
        return self._bid
    @property    
    def time_left(self):
        return self._time_left
    @property    
    def url(self):
        return self._url
    @property    
    def img_url(self):
        return self._img_url