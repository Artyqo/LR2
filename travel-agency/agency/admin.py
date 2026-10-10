from django.contrib import admin
from .models import (
    News, CompanyInfo, FAQ, Vacancy, Review, PromoCode, Country, Hotel,
    Employee, Client, Tour, Order, Partner, Banner, Cart, CartItem, OrderItem, Inquiry,
)


# Настройка встроенного (Inline) редактирования
class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 1  # пустых строк для добавления отелей прямо внутри страны


class TourInline(admin.TabularInline):
    model = Tour
    extra = 1  # пустых строк для добавления туров прямо внутри отеля


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'climate_summer', 'climate_winter')
    search_fields = ('name',)
    inlines = [HotelInline]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'stars', 'price_per_day')
    list_filter = ('country', 'stars')
    search_fields = ('name',)
    inlines = [TourInline]


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'duration_weeks', 'departure_date', 'is_hot')
    list_filter = ('duration_weeks', 'is_hot', 'hotel__country')
    search_fields = ('title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'created_at', 'total_cost')
    list_filter = ('created_at', 'employee')
    filter_horizontal = ('tours',)
    inlines = [OrderItemInline]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_url', 'sort_order', 'is_active')
    list_filter = ('is_active',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('client', 'updated_at')
    inlines = [CartItemInline]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'country', 'departure_date', 'budget', 'contact_method', 'created_at')
    list_filter = ('contact_method', 'meal_plan', 'with_children', 'country')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'created_at'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'phone', 'email')
    search_fields = ('full_name', 'position', 'email')


# Регистрация остальных базовых моделей
admin.site.register(News)
admin.site.register(CompanyInfo)
admin.site.register(FAQ)
admin.site.register(Vacancy)
admin.site.register(Review)
admin.site.register(PromoCode)
admin.site.register(Client)