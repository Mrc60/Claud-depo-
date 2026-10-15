"""3D deneme: dönen Dünya + İstanbul -> Pire deniz rotası (20 sn, 1080x1920, Cycles CPU).
Kullanım: blender -b -P deneme3d/kurtulus_rota.py -- <doku.jpg> <font.otf> <cikti_klasoru>"""
import bpy, math, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
DOKU, FONT, OUT = argv[0], argv[1], argv[2]
FPS, N = 24, 480

def P(lat, lon, r=1.0):
    la, lo = math.radians(lat), math.radians(lon)
    return Vector((r * math.cos(la) * math.cos(lo), r * math.cos(la) * math.sin(lo), r * math.sin(la)))

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 24
sc.cycles.use_adaptive_sampling = True
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, N
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = OUT + "/f_"
sc.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in sc.view_settings.bl_rna.properties["view_transform"].enum_items] else "Filmic"

# Arka plan: koyu lacivert
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.006, 0.014, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0

# Dünya küresi: doku eşdikdörtgen; koordinat nesne uzayından enlem/boylamla hesaplanır
bpy.ops.mesh.primitive_uv_sphere_add(segments=256, ring_count=128, radius=1.0)
dunya = bpy.context.object; bpy.ops.object.shade_smooth()
m = bpy.data.materials.new("Dunya"); m.use_nodes = True; nt = m.node_tree; nd = nt.nodes
bsdf = nd["Principled BSDF"]; bsdf.inputs["Roughness"].default_value = 0.75
tc = nd.new("ShaderNodeTexCoord"); sep = nd.new("ShaderNodeSeparateXYZ")
nt.links.new(tc.outputs["Object"], sep.inputs[0])
def math_node(op, a=None, b=None, va=None, vb=None):
    n = nd.new("ShaderNodeMath"); n.operation = op
    if a is not None: nt.links.new(a, n.inputs[0])
    else: n.inputs[0].default_value = va
    if b is not None: nt.links.new(b, n.inputs[1])
    elif vb is not None: n.inputs[1].default_value = vb
    return n
lon = math_node("ARCTAN2", sep.outputs["Y"], sep.outputs["X"])
u = math_node("ADD", math_node("DIVIDE", lon.outputs[0], vb=2 * math.pi).outputs[0], vb=0.5)
lat = math_node("ARCSINE", sep.outputs["Z"])
v = math_node("ADD", math_node("DIVIDE", lat.outputs[0], vb=math.pi).outputs[0], vb=0.5)
comb = nd.new("ShaderNodeCombineXYZ")
nt.links.new(u.outputs[0], comb.inputs[0]); nt.links.new(v.outputs[0], comb.inputs[1])
img = nd.new("ShaderNodeTexImage"); img.image = bpy.data.images.load(DOKU); img.interpolation = "Cubic"
nt.links.new(comb.outputs[0], img.inputs[0]); nt.links.new(img.outputs["Color"], bsdf.inputs["Base Color"])
dunya.data.materials.append(m)

# Atmosfer parıltısı
bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=1.025)
atm = bpy.context.object; bpy.ops.object.shade_smooth()
ma = bpy.data.materials.new("Atm"); ma.use_nodes = True; an = ma.node_tree.nodes; al = ma.node_tree.links
for n in list(an): an.remove(n)
out = an.new("ShaderNodeOutputMaterial"); mix = an.new("ShaderNodeMixShader")
tr = an.new("ShaderNodeBsdfTransparent"); em = an.new("ShaderNodeEmission")
em.inputs[0].default_value = (0.25, 0.55, 1.0, 1); em.inputs[1].default_value = 2.5
lw = an.new("ShaderNodeLayerWeight"); lw.inputs[0].default_value = 0.12
ramp = an.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.55
al.new(lw.outputs["Facing"], ramp.inputs[0]); al.new(ramp.outputs[0], mix.inputs[0])
al.new(tr.outputs[0], mix.inputs[1]); al.new(em.outputs[0], mix.inputs[2]); al.new(mix.outputs[0], out.inputs[0])
ma.blend_method = "BLEND" if hasattr(ma, "blend_method") else None
atm.data.materials.append(ma)

# Güneş ışığı
bpy.ops.object.light_add(type="SUN", location=(0, 0, 0))
sun = bpy.context.object; sun.data.energy = 4.0
sun.rotation_euler = (P(25, 60) * -1).to_track_quat("-Z", "Y").to_euler()

def emis(name, rgb, s=6.0):
    mt = bpy.data.materials.new(name); mt.use_nodes = True; tn = mt.node_tree.nodes
    for n in list(tn): tn.remove(n)
    e = tn.new("ShaderNodeEmission"); e.inputs[0].default_value = (*rgb, 1); e.inputs[1].default_value = s
    o = tn.new("ShaderNodeOutputMaterial"); mt.node_tree.links.new(e.outputs[0], o.inputs[0]); return mt
AMBER = (1.0, 0.62, 0.15)

# Deniz rotası: İstanbul -> Marmara -> Çanakkale Boğazı -> Ege -> Pire (yaklaşık noktalar)
YOL = [(41.00, 28.98), (40.85, 28.40), (40.62, 27.45), (40.42, 26.70), (40.20, 26.42), (40.02, 26.18),
       (39.60, 25.70), (39.00, 25.05), (38.45, 24.55), (38.05, 24.15), (37.94, 23.64)]
cu = bpy.data.curves.new("Rota", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.0016
cu.bevel_resolution = 4; cu.use_fill_caps = True
sp = cu.splines.new("POLY"); sp.points.add(len(YOL) - 1)
for i, (la, lo) in enumerate(YOL): sp.points[i].co = (*P(la, lo, 1.004), 1)
rota = bpy.data.objects.new("Rota", cu); sc.collection.objects.link(rota)
cu.materials.append(emis("RotaM", AMBER, 8))
F_ROTA0, F_ROTA1 = 270, 420
cu.bevel_factor_end = 0.0; cu.keyframe_insert("bevel_factor_end", frame=F_ROTA0)
cu.bevel_factor_end = 1.0; cu.keyframe_insert("bevel_factor_end", frame=F_ROTA1)

# Rota üzerinde ilerleyen gemi noktası
uz = [0.0]
for a, b in zip(YOL, YOL[1:]): uz.append(uz[-1] + (P(*a) - P(*b)).length)
def nokta(t):
    hedef = t * uz[-1]
    for i in range(len(YOL) - 1):
        if uz[i + 1] >= hedef:
            k = (hedef - uz[i]) / max(1e-9, uz[i + 1] - uz[i])
            return P(*YOL[i], 1.006).lerp(P(*YOL[i + 1], 1.006), k)
    return P(*YOL[-1], 1.006)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0045, location=nokta(0))
gemi = bpy.context.object; gemi.data.materials.append(emis("GemiM", (1, 0.95, 0.8), 15))
for f in range(F_ROTA0, F_ROTA1 + 1, 6):
    gemi.location = nokta((f - F_ROTA0) / (F_ROTA1 - F_ROTA0)); gemi.keyframe_insert("location", frame=f)
gemi.scale = (0, 0, 0); gemi.keyframe_insert("scale", frame=F_ROTA0 - 1)
gemi.scale = (1, 1, 1); gemi.keyframe_insert("scale", frame=F_ROTA0)

# Kamera ve hedef
hedef = bpy.data.objects.new("Hedef", None); sc.collection.objects.link(hedef)
cam_d = bpy.data.cameras.new("Cam"); cam_d.lens = 35; cam_d.clip_start = 0.01
cam = bpy.data.objects.new("Cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
c = cam.constraints.new("TRACK_TO"); c.target = hedef; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
MERKEZ = (39.45, 26.3)
def kam(f, la, lo, r, hla=None, hlo=None, hr=0.0):
    cam.location = P(la, lo, r); cam.keyframe_insert("location", frame=f)
    hedef.location = P(hla, hlo, hr) if hla is not None else Vector((0, 0, 0)); hedef.keyframe_insert("location", frame=f)
# 1) uzaktan dünya döner (kamera yörüngede)  2) Ege'ye yaklaşır  3) rota çizilirken bekler
for i, f in enumerate(range(1, 151, 15)):
    kam(f, 18 + i * 1.2, -40 + i * 6.2, 3.3)
kam(150, 30, 22, 3.0)
kam(265, 35.6, 26.5, 1.30, *MERKEZ, 1.0)
kam(N, 35.2, 26.1, 1.27, *MERKEZ, 1.0)
for o in (cam, hedef):
    for fc in o.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation = "BEZIER"

# Şehir işaretleri ve yazıları (Türkçe karakterli yazı tipi)
font = bpy.data.fonts.load(FONT)
def isaret(ad, la, lo, dx, dz):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0035, location=P(la, lo, 1.004))
    bpy.context.object.data.materials.append(emis("Sehir" + ad, AMBER, 10))
    td = bpy.data.curves.new(ad, "FONT"); td.body = ad; td.font = font; td.size = 0.014; td.align_x = "CENTER"
    t = bpy.data.objects.new("T" + ad, td); sc.collection.objects.link(t)
    t.location = P(la + dz, lo + dx, 1.012)
    tc_ = t.constraints.new("TRACK_TO"); tc_.target = cam; tc_.track_axis = "TRACK_Z"; tc_.up_axis = "UP_Y"
    td.materials.append(emis("Yazi" + ad, (1, 1, 1), 4))
    t.scale = (0, 0, 0); t.keyframe_insert("scale", frame=240)
    t.scale = (1, 1, 1); t.keyframe_insert("scale", frame=262)
isaret("İSTANBUL", 41.00, 28.98, 0.0, 0.55)
isaret("PİRE", 37.94, 23.64, 0.0, -0.75)

bpy.ops.render.render(animation=True)
