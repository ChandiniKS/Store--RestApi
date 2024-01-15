from decimal import Decimal
from store.models import Product, Collection, Review,Cart,CartItem
from rest_framework import serializers

class SimpleProuctSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=fields = ['title','unit_price']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

   
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProuctSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product','quantity','price_of_item']

    price_of_item=serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self,product:Product):
        return product.quantity * product.product.unit_price
    
class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True) 
    grand_total=serializers.SerializerMethodField(method_name='get_grand_total')

    def get_grand_total(self,cart):
        sum=0
        for item in cart.items.all():
            sum+=((item.quantity)*(item.product.unit_price))
        return sum

    class Meta:
        model=Cart
        fields=['id','items','grand_total']  # a cart has many items so we use a list of primary
        
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()

    def save(self, **validated_data):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']

        def validate_product_id(self,value):
            if not Product.objects.filter(pk=value).exists():
                raise serializers.ValidationError("The provided product does not exist")
            return value

        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance
    

    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    


class UpdateCartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']