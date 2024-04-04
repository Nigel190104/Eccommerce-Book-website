from decimal import Decimal

from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviours that
    can be inherited or overrided, as necessary.
    """
    #reserved method
    #in terms of object orientated program when we create a new copty of the object which is the basket
    #whenev3r we create a basket object the function below will be initialised and run
    #this is going to be intialised
    #this will check if a session exists ansd make sure it is a session already if it doesnt then it will create one
    #we want to call this method on every page that the user goes to and when the user goes to 
    # a different page the session will be created and prepared so that they can put any item they want into the basket
    def __init__(self, request):
       self.session = request.session
       basket = self.session.get('sKey')
       if 'sKey' not in request.session:
           basket = self.session['sKey'] = {}
       self.basket = basket

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = product.id
    
        if product_id not in self.basket:
           self.basket[product_id] = {'price': str(product.price), 'qty':int(qty)}
           
        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        try:
            return sum(item['qty'] for item in self.basket.values())
        except (KeyError, TypeError):
            return 0
        
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        print(type(product_id))
        if product_id in self.basket:
            del self.basket[product_id] 
            self.save()



    def update(self, product, qty):
        """
        update values in session data
        """

        product_id= product

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()
        
    def save(self):
        self.session.modified = True