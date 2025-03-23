def create_category(form):
    return form.save()

def delete_category(category):
    category.delete()
