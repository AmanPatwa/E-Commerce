from django.shortcuts import render, get_object_or_404
from .models import Item,Order,OrderItem,BillingAddress
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required

def item_list(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request,'home-page.html',context)

class CheckoutView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        # print(form)
        return render(self.request,'checkout-page.html',context)
    
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or NONE)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address , 
                    appartment_address = appartment_address ,
                    country = country,
                    zip = zip
                )
                billing_address.save()
                order.billing_address= billing_address
                order.save()
            
            return redirect('core:item-checkout')
        
            
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect('core:order-summary')
        
def item(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request,'product-page.html',context)


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home-page.html'
    context_object_name = 'items'

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                'orders':order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You do not have an active order")
            return redirect('/')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'
    context_object_name = 'item'

@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Item,pk = pk)
    order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The quantity of the order is changed")
            return redirect('core:order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, "Your order has been successsfully placed")
            return redirect('core:order-summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user,ordered_date= ordered_date)
        order.items.add(order_item)
        messages.info(request, "Your order has been successsfully placed")
        return redirect('core:order-summary')

    return redirect('core:order-summary')

@login_required
def remove_from_cart(request,pk):
    item = get_object_or_404(Item,pk = pk)
    order_qs = Order.objects.filter(user = request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered = False)[0]
            
            # order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Your order has been successsfully removed")
            return redirect('core:order-summary')
        else:
            messages.info(request, "The item is not in your cart")
            return redirect('core:order-summary')
    else:
        messages.info(request, "Your cart is empty")
        return redirect('core:order-summary')

    return redirect('core:order-summary')

@login_required
def remove_single_item_from_cart(request,pk):
    item = get_object_or_404(Item,pk = pk)
    order_item = OrderItem.objects.get(item = item, user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user,ordered = False)
    if order_qs.exists() and order_item.quantity>1:
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists():
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "The quantity of the order is changed")
            return redirect('core:order-summary')
        else:
            # order.items.add(order_item)
            messages.info(request, "Please Place the order")
            return redirect('core:product',pk=pk)

    else:
        order_item.delete()
    #     ordered_date = timezone.now()
    #     order = Order.objects.create(user = request.user,ordered_date= ordered_date)
    #     order.items.add(order_item)
    #     messages.info(request, "Your order has been successsfully placed")
    #     return redirect('core:product',pk=pk)

    return redirect('core:order-summary')
