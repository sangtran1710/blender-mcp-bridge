import bpy

def list_objects():
    print(f"Scene: {bpy.context.scene.name}")
    print("Objects in Scene:")
    for obj in bpy.context.scene.objects:
        print(f"- {obj.name} (Type: {obj.type}, Visible: {obj.visible_get()})")
    return "List Complete"

try:
    list_objects()
except Exception as e:
    import traceback
    traceback.print_exc()
