def get_related_objects(instance):
    """
    get all related object of a certain object instance.
    """
    related_objects = {}

    for field in instance._meta.get_fields():

        if field.one_to_many or field.one_to_one or field.many_to_many:
            related_name = field.name  # name of related field

            try:
                related_data = getattr(instance, related_name)

                if field.one_to_one:
                    related_objects[related_name] = related_data  # OneToOne

                elif field.many_to_many:
                    related_objects[related_name] = list(
                        related_data.all()
                    )  # ManyToMany : a list of objects

                elif field.one_to_many:
                    related_objects[related_name] = list(
                        related_data.all()
                    )  # ForeignKey

            except Exception as e:
                print(f"Can not get related object {related_name} : {e}")

    return related_objects


def delete_related_objects(instance):
    related_objects = get_related_objects(instance=instance)
    for ralated_name, objects in related_objects:
        if isinstance(objects, list):
            for object in objects:
                print("About to delete : ", object)
                object.delete()

        print("About to delete : ", objects)
        objects.delete()
