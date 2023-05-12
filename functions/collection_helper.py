import bpy


def collection(name):
    coll = bpy.data.collections.get(name)
    if coll == None:
        coll = bpy.data.collections.new(name)
    return coll

def link(ob,coll):
    try:
        coll.children.link(ob)
    except:
        pass
    try:
        coll.objects.link(ob)
    except:
        pass

def move(ob,from_,to_):
    try:
        to_.children.link(ob)
    except:
        pass
    try:
        to_.objects.link(ob)
    except:
        pass

    try:
        from_.children.unlink(ob)
    except:
        pass
    try:
        from_.objects.unlink(ob)
    except:
        pass   

# collection_helper = ImportFromAddonDir('collection_helper','functions')   

# collection = collection_helper.collection
# link = collection_helper.link
# move = collection_helper.move