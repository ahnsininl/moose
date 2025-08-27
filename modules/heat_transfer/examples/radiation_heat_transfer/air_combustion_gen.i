[Mesh]
  # [hex_1]
  #   type = PolygonConcentricCircleMeshGenerator
  #   num_sides = 6
  #   num_sectors_per_side = '4 4 4 4 4 4'
  #   background_intervals = 2
  #   ring_radii = 4.0
  #   ring_intervals = 2

  #   # ring_inner_boundary_layer_biases = '1.25'
  #   # ring_inner_boundary_layer_intervals = '10'
  #   # ring_inner_boundary_layer_widths = '0.1'
  #   # ring_outer_boundary_layer_biases = '0.8'
  #   # ring_outer_boundary_layer_intervals = 10
  #   # ring_outer_boundary_layer_widths = '0.1'

  #   ring_block_ids = '10 15'
  #   ring_block_names = 'center_tri center'

  #   background_block_ids = 20
  #   # background_block_names = background
  #   polygon_size = 5.0
  #   # preserve_volumes = on
  # []

  [hex_1]
    type = ConcentricCircleMeshGenerator
    num_sectors = 6
    radii = '0.02 0.04 0.3'
    rings = '5 12 6'
    has_outer_square = off
    # pitch = 1.42063
    #portion = left_half
    preserve_volumes = off
    smoothing_max_it = 3
  []

  [ed0]
    type = BlockDeletionGenerator
    input = hex_1
    block = '1'
  []

  [ext]
    type = MeshExtruderGenerator
    input = ed0
    extrusion_vector = '0 0 20'
    num_layers = 20
  []
[]
