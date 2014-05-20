from bookmark.models import BookMark,Link
from django.contrib.auth.models import User
user = User.objects.get(id = 1)
link = Link.objects.get(id = 2)
bookmark = BookMark(title = 'Sina Pub',user = user,link = link)
bookmark.save()