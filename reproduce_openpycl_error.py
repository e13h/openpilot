import pyopencl as cl

ctx = cl.create_some_context()
with open("/workspaces/openpilot/tools/sim/rgb_to_nv12.cl", "r", encoding="utf-8") as f:
    converter = f.read()
prg = cl.Program(ctx, converter)
W, H = 1928, 1208
cl_arg = f" -DHEIGHT={H} -DWIDTH={W} -DRGB_STRIDE={W * 3} -DUV_WIDTH={W // 2} -DUV_HEIGHT={H // 2} -DRGB_SIZE={W * H} -DCL_DEBUG "
prg_b = prg.build(cl_arg)
prg_b.rgb_to_nv12

