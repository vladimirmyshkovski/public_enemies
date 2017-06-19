from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from geoposition.fields import GeopositionField
from hitcount.models import HitCountMixin
import secretballot

# Create your models here.
@python_2_unicode_compatible
class Enemy(models.Model, HitCountMixin):
	first_name = models.CharField(max_length=255, null=True, verbose_name=_('Имя врага'))
	last_name = models.CharField(max_length=255, null=True, verbose_name=_('Его фамилия'))

	avatar = models.ImageField(upload_to = 'enemy/', null=True, verbose_name=_('Фотография'))

	description = models.CharField(max_length=1024, null=True, verbose_name=_('Описания злодеяний'))

	country = models.ForeignKey('cities_light.Country', null=True, verbose_name=_('Страна проживания'))
	city = models.ForeignKey('cities_light.City', null=True, verbose_name=_('Город проживания'))

	address = GeopositionField(null=True, verbose_name=_('Адресс'))


secretballot.enable_voting_on(Enemy)