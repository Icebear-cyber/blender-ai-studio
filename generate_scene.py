# Blender AI Studio - Scene Generator
# Automate 3D scene creation with Blender Python API

import bpy
import random
import math

def clear_scene():
    """Remove all default objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("Scene cleared")

def create_camera(location=(7, -7, 5), target=(0, 0, 0)):
    """Create and position a camera"""
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    
    # Point camera at target
    direction = [target[i] - location[i] for i in range(3)]
    rot_quat = direction_to_quaternion(direction)
    camera.rotation_euler = rot_quat.to_euler()
    
    bpy.context.scene.camera = camera
    print(f"Camera created at {location}")
    return camera

def direction_to_quaternion(direction):
    """Convert direction vector to quaternion"""
    import mathutils
    up = mathutils.Vector((0, 0, 1))
    direction = mathutils.Vector(direction).normalized()
    axis = up.cross(direction)
    angle = math.acos(up.dot(direction))
    return mathutils.Quaternion(axis, angle)

def create_lighting(type='SUN', energy=5.0, location=(5, 5, 5)):
    """Add lighting to the scene"""
    bpy.ops.object.light_add(type=type, location=location)
    light = bpy.context.object
    light.data.energy = energy
    print(f"{type} light created with energy {energy}")
    return light

def create_material(name="Material", color=(0.8, 0.2, 0.1, 1.0), metallic=0.0, roughness=0.5):
    """Create a PBR material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get('Principled BSDF')
    
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
    
    print(f"Material '{name}' created")
    return mat

def create_cube(location=(0, 0, 0), scale=(1, 1, 1), material=None):
    """Create a cube with optional material"""
    bpy.ops.mesh.primitive_cube_add(location=location, scale=scale)
    cube = bpy.context.object
    
    if material:
        if cube.data.materials:
            cube.data.materials[0] = material
        else:
            cube.data.materials.append(material)
    
    print(f"Cube created at {location}")
    return cube

def create_sphere(location=(0, 0, 0), radius=1.0, material=None):
    """Create a UV sphere"""
    bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=radius)
    sphere = bpy.context.object
    
    if material:
        if sphere.data.materials:
            sphere.data.materials[0] = material
        else:
            sphere.data.materials.append(material)
    
    print(f"Sphere created at {location}")
    return sphere

def create_plane(location=(0, 0, 0), size=10, material=None):
    """Create a ground plane"""
    bpy.ops.mesh.primitive_plane_add(location=location, size=size)
    plane = bpy.context.object
    
    if material:
        if plane.data.materials:
            plane.data.materials[0] = material
        else:
            plane.data.materials.append(material)
    
    print(f"Plane created at {location}")
    return plane

def generate_random_scene(num_objects=5):
    """Generate a random 3D scene with multiple objects"""
    print("\n" + "="*50)
    print("Blender AI Studio - Random Scene Generator")
    print("="*50)
    
    # Clear scene
    clear_scene()
    
    # Add camera
    create_camera()
    
    # Add lighting
    create_lighting('SUN', energy=3.0, location=(5, 5, 10))
    create_lighting('AREA', energy=100, location=(-5, -5, 5))
    
    # Create ground
    ground_mat = create_material("Ground", color=(0.2, 0.2, 0.2, 1.0), roughness=0.8)
    create_plane(location=(0, 0, 0), size=20, material=ground_mat)
    
    # Generate random objects
    for i in range(num_objects):
        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)
        z = random.uniform(0.5, 3)
        
        color = (random.random(), random.random(), random.random(), 1.0)
        metallic = random.uniform(0, 1)
        roughness = random.uniform(0.1, 0.9)
        
        mat = create_material(f"Mat_{i}", color=color, metallic=metallic, roughness=roughness)
        
        if random.choice([True, False]):
            create_cube(location=(x, y, z), scale=(random.uniform(0.5, 2), ) * 3, material=mat)
        else:
            create_sphere(location=(x, y, z), radius=random.uniform(0.5, 1.5), material=mat)
    
    print("\nScene generation complete!")
    print(f"Total objects: {num_objects + 3}  (including camera, lights, ground)")
    print("="*50)

if __name__ == "__main__":
    # Run the generator
    generate_random_scene(num_objects=8)
    
    # Render settings
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    
    print("\nRender settings configured (1920x1080, Cycles, 128 samples)")
    print("Ready to render! (Rendering > Render Image)")
