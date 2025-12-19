import bpy

def cleanup():
    print("Starting Cleanup...")
    
    # Stop Animation
    if bpy.ops.screen.animation_cancel.poll():
        bpy.ops.screen.animation_cancel(restore_frame=False)

    # 1. Ensure Object Mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass 

    # 2. Delete All Objects
    # Unhide/Unlock all so we can select them
    for obj in bpy.data.objects:
        obj.hide_select = False
        obj.hide_viewport = False
        obj.hide_render = False

    # Deselect all first to be clean
    bpy.ops.object.select_all(action='DESELECT')
    # Select all
    bpy.ops.object.select_all(action='SELECT')
    # Delete
    bpy.ops.object.delete()
    
    # 3. Purge Orphans (Recursive)
    # We do this a few times because deleting one thing might orphan another
    for i in range(5):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

    # 4. Remove all collections
    # Unlink from scene first
    for c in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(c)
    
    # Remove from data if unused
    for c in bpy.data.collections:
        if c.users == 0:
            bpy.data.collections.remove(c)

    print("Cleanup Complete: All objects deleted and orphans purged.")
    return "Cleanup Complete"

try:
    result = cleanup()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error during cleanup: {e}")
