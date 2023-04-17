from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


class AutomobilioModelis(models.Model):
    marke = models.CharField(_('Make'), max_length=100)
    modelis = models.CharField(_('Model'), max_length=100)
    metai = models.CharField(_('Year'), max_length=4)
    variklis = models.CharField(_('Engine'), max_length=10)

    def __str__(self):
        return f'{self.marke} {self.modelis} ({self.metai}, {self.variklis})'

    class Meta:
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')


class Paslauga(models.Model):
    pavadinimas = models.CharField(_('cdName'), max_length=100, help_text=_('Enter the name of the service (eg oil change)'))
    paslaugos_kaina = models.DecimalField(_('Price'), max_digits=12, decimal_places=2, help_text=_('Enter the price of the service'))

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(_('License Plate'), max_length=7)
    automobilio_modelis = models.ForeignKey(to=AutomobilioModelis, on_delete=models.SET_NULL, null=True, verbose_name='Automobilis')
    vin_kodas = models.CharField(_('VIN code'), max_length=20)
    klientas = models.CharField(_('Customer'), max_length=20)
    cover = models.ImageField(_('Photo'), upload_to='automobiliai', null=True)
    aprasymas = HTMLField(_('Description'), default='')

    def __str__(self):
        return f'{self.valstybinis_nr} | {self.automobilio_modelis}'

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')


class Uzsakymas(models.Model):
    data = models.DateTimeField(_('Date'), auto_now_add=True)
    automobilis = models.ForeignKey(to="Automobilis", verbose_name=_("Vehicle"), on_delete=models.CASCADE)
    # suma = models.DecimalField('Suma', max_digits=12, decimal_places=2, default=0, null=True)
    aprasymas = HTMLField(_('Description of the problem'), default='')
    vartotojas = models.ForeignKey(to=User, verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    terminas = models.DateField(_('Deadline'), null=True, blank=True)

    @property
    def ar_baigesi_terminas(self):
        if self.terminas and date.today() > self.terminas:
            return True
        return False

    def suma(self):
        suma = 0
        eilutes = self.uzsakymo_eilutes.all()
        for eilute in eilutes:
            suma += eilute.kaina()
        return suma

    LOAN_STATUS = (
        ('p', _("Confirmed")),
        ('v', _("In Progress")),
        ('i', _("Done")),
        ('a', _("Canceled")),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text=_("Status"),
    )

    # def save(self):
    #     suma = 0
    #     eilutes = self.uzsakymo_eilutes.all()
    #     for eilute in eilutes:
    #         suma += eilute.kaina()
    #     self.suma = suma
    #     super().save()

    def __str__(self):
        return f"{self.data.strftime('%Y-%m-%d %H:%M:%S')} >>> {self.automobilis}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-data']


class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey(to="Paslauga", verbose_name=_("Service"), on_delete=models.SET_NULL, null=True)
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name=_("Order"), on_delete=models.CASCADE, related_name='uzsakymo_eilutes')
    kiekis = models.IntegerField(_("Quantity"))
    # kaina = models.DecimalField('Kaina', max_digits=12, decimal_places=2, default=0, null=True)

    def __str__(self):
        return f'{self.uzsakymas.data} - {self.paslauga}'

    def kaina(self):
         return self.kiekis * self.paslauga.paslaugos_kaina

    # def save(self):
    #     self.kaina = self.kiekis * self.paslauga.paslaugos_kaina
    #     super().save()

    class Meta:
        verbose_name = _("Orderline")
        verbose_name_plural = _("Orderlines")


class UzsakymuAtsiliepimai(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, blank=True)
    komentatorius = models.ForeignKey(to=User, verbose_name=_("Commentator"), on_delete=models.SET_NULL, null=True, blank=True)
    sukurimo_data = models.DateTimeField(auto_now_add=True)
    atsiliepimas = models.TextField(_("Comment"), max_length=2000)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-sukurimo_data']


class Profilis(models.Model):
    user = models.OneToOneField(to=User, verbose_name=_("User"), on_delete=models.CASCADE)
    nuotrauka = models.ImageField(verbose_name=_("Photo"), default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)