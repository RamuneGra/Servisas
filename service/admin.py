from django.contrib import admin
from .models import AutomobilioModelis, Paslauga, Automobilis, Uzsakymas, UzsakymoEilute, UzsakymuAtsiliepimai, Profilis
from django.utils.translation import gettext_lazy as _

class AutomobilioModelisAdmin(admin.ModelAdmin):
    list_display = ('marke', 'modelis', 'metai', 'variklis')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'paslaugos_kaina')
    search_fields = ('pavadinimas',)


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis__marke', 'automobilio_modelis__modelis', 'automobilio_modelis__metai', 'automobilio_modelis__variklis')
    search_fields = ('valstybinis_nr', 'vin_kodas', 'klientas', 'automobilio_modelis__marke', 'automobilio_modelis__modelis', 'automobilio_modelis__metai')
    fieldsets = (
        (_('Vehicle details'), {'fields': ('automobilio_modelis', 'valstybinis_nr', 'vin_kodas', 'cover', 'aprasymas')}),
        (_('Customer'), {'fields': ('klientas', )}),
    )

class UzsakymoEiluteInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('automobilis', 'data', 'suma', 'vartotojas', 'terminas', 'status')
    inlines = [UzsakymoEiluteInline]
    list_filter = ('automobilis', 'data', 'status', 'terminas')
    search_fields = ('automobilis__valstybinis_nr', 'automobilis__klientas', 'data')
    fieldsets = (
        (_('Order details'), {'fields': ('status', 'terminas', 'aprasymas')}),
        (_('Vehicle details'), {'fields': ('automobilis', 'vartotojas')}),
    )

class UzsakymoEiluteAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'paslauga', 'kiekis', 'kaina')
    list_filter = ('uzsakymas__data', 'uzsakymas', 'paslauga', 'kiekis')
    fieldsets = (
        (_('Order'), {'fields': ('uzsakymas',)}),
        (_('Information'), {'fields': ('paslauga', 'kiekis')}),
    )

class UzsakymuAtsiliepimaiAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'sukurimo_data', 'komentatorius', 'atsiliepimas')


admin.site.register(UzsakymuAtsiliepimai, UzsakymuAtsiliepimaiAdmin)
admin.site.register(AutomobilioModelis, AutomobilioModelisAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute, UzsakymoEiluteAdmin)
admin.site.register(Profilis)

