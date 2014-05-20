from bookmark.models import Tag,BookMark,Link
bookmark = BookMark.objects.get(id = 1)
print bookmark.link.url
# tag1 = Tag(name = 'book')
# tag1.save()
# bookmark.tag_set.add(tag1)
# tag2 = Tag(name = 'publisher')
# tag2.save()
# bookmark.tag_set.add(tag2)
print bookmark.tag_set.all()