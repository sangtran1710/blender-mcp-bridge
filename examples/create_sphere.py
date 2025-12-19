import bpy

def create_sphere():
    print("Creating Sphere...")
    # Create UV Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1.0, 
        location=(0, 0, 0)
    )
    print("Sphere Created successfully.")
    return "Sphere Created"

try:
    result = create_sphere()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error creating sphere: {e}")
