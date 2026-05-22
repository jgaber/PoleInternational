import polib
po = polib.pofile('locale/fr/LC_MESSAGES/django.po')
po.save_as_mofile('locale/fr/LC_MESSAGES/django.mo')
print("Conversion successful")
