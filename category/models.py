# category.models.py

from django.db import models

from tagulous.models import TagField
from mptt.models import MPTTModel, TreeForeignKey


NULL_AND_BLANK = {'null': True, 'blank': True}
UNIQUE_AND_DB_INDEX = {'unique': True, 'db_index': True}


class Category(MPTTModel):
    parent = TreeForeignKey(to='self', related_name='children', on_delete=models.CASCADE, db_index=True, **NULL_AND_BLANK)
    name = models.CharField(verbose_name='catégorie', max_length=120, db_index=True)
    keywords = TagField(verbose_name='mot clés', blank=True)
    slug = models.SlugField(verbose_name='lien', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        app_label = 'category'
        verbose_name = 'catégorie'
        verbose_name_plural = 'catégories'
        unique_together = (('parent', 'slug',))


    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(ascending=True, include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
        slugs = []

        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.name

    def __repr__(self):
       return self.__str__()

    # def get_category_url(self):
    #     return reverse('category_detail', kwargs={'slug': str(self.slug)})
