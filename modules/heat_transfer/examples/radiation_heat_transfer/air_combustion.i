n1 = 1.46
n2 = 1.00

alpha = 0.914
alpha1 =  0.084075389781548382
alpha2 =  0.872433935441263020
beta1 = -0.08086509944859642
beta2 = -0.29284032175563224
eta1 =  -2.6234175064678195
eta2 = 9.9471473598607409

k = 1
h = 0.001
Tb = 300
T0 = 1000
epsilon = 1.0
endt = 0.0001
dt = 2.5e-5#0.00005 #2.5e-5#

nu_min = 1e-2
nu1 = 3.11e13
nu2 = 5.13e13
nu3 = 8.21e13
nu4 = 1.37e14
nu_max = 1e16

kappa1to2 = 1.0
kappa2to3 = 500.0
kappa3to4 = 75.0

[Mesh]
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

  # [ed0]
  #   type = BlockDeletionGenerator
  #   input = hex_1
  #   block = '1'
  # []

  [ext]
    type = MeshExtruderGenerator
    input = hex_1
    extrusion_vector = '0 0 20'
    num_layers = 20
  []
[]

[Problem]
  nl_sys_names = 't
                  psi11 psi12 psi13
                  psi21 psi22 psi23
                  P_H2O'

  verbose_setup = true
[]

[Variables]
  [T]
    type = MooseVariableFVReal
    initial_condition = ${T0}
    solver_sys = 't'
  []

  [psi11]
    type = MooseVariableFVReal
    solver_sys = 'psi11'
  []

  [psi21]
    type = MooseVariableFVReal
    solver_sys = 'psi21'
  []

  [psi12]
    type = MooseVariableFVReal
    solver_sys = 'psi12'
  []

  [psi22]
    type = MooseVariableFVReal
    solver_sys = 'psi22'
  []

  [psi13]
    type = MooseVariableFVReal
    solver_sys = 'psi13'
  []

  [psi23]
    type = MooseVariableFVReal
    solver_sys = 'psi23'
  []
[]

[FVKernels]
  [diffusion11]
    type = FVSP3ThermalRadiationDiffusion
    variable = psi11
    epsilon = ${epsilon}
    kappa = ${kappa1to2}
    order = first
  []

  [diffusion21]
    type = FVSP3ThermalRadiationDiffusion
    variable = psi21
    epsilon = ${epsilon}
    kappa = ${kappa1to2}
    order = second
  []

  [diffusion12]
    type = FVSP3ThermalRadiationDiffusion
    variable = psi12
    epsilon = ${epsilon}
    kappa = ${kappa2to3}
    order = first
  []

  [diffusion22]
    type = FVSP3ThermalRadiationDiffusion
    variable = psi22
    epsilon = ${epsilon}
    kappa = ${kappa2to3}
    order = second
  []

  [diffusion13]
    type = FVSP3ThermalRadiationDiffusion
    variable = psi13
    epsilon = ${epsilon}
    kappa = ${kappa3to4}
    order = first
  []

  [diffusion23]
    type = FVSP3ThermalRadiationDiffusion
    variable = psi23
    epsilon = ${epsilon}
    kappa = ${kappa3to4}
    order = second
  []

  [sink11]
    type = FVSP3ThermalRadiationSourceSink
    variable = psi11
    T = 'T'
    nu = ${nu1}
    nu_low =${nu1}
    nu_high = ${nu2}
    refraction_index = ${n1}
    kappa = ${kappa1to2}
  []

  [sink21]
    type = FVSP3ThermalRadiationSourceSink
    variable = psi21
    T = 'T'
    nu = ${nu1}
    nu_low = ${nu1}
    nu_high = ${nu2}
    refraction_index = ${n1}
    kappa = ${kappa1to2}
  []

  [sink12]
    type = FVSP3ThermalRadiationSourceSink
    variable = psi12
    T = 'T'
    nu = ${nu2}
    nu_low =${nu2}
    nu_high = ${nu3}
    refraction_index = ${n1}
    kappa = ${kappa2to3}
  []

  [sink22]
    type = FVSP3ThermalRadiationSourceSink
    variable = psi22
    T = 'T'
    nu = ${nu2}
    nu_low = ${nu2}
    nu_high = ${nu3}
    refraction_index = ${n1}
    kappa = ${kappa2to3}
  []

  [sink13]
    type = FVSP3ThermalRadiationSourceSink
    variable = psi13
    T = 'T'
    nu = ${nu3}
    nu_low =${nu3}
    nu_high = ${nu4}
    refraction_index = ${n1}
    kappa = ${kappa3to4}
  []

  [sink23]
    type = FVSP3ThermalRadiationSourceSink
    variable = psi23
    T = 'T'
    nu = ${nu3}
    nu_low = ${nu3}
    nu_high = ${nu4}
    refraction_index = ${n1}
    kappa = ${kappa3to4}
  []

  [energy_source]
    type = FVSP3TemperatureSourceSink
    variable = T
    absorptivities = '${kappa1to2} ${kappa2to3} ${kappa3to4}'
    psi_1 = 'psi11 psi12 psi13'
    psi_2 = 'psi21 psi22 psi23'
    # force_boundary_execution = true
  []

  [energy_time]
    type = FVTimeKernel
    variable = T
  []

  [energy_diffusion]
    type = FVDiffusion
    variable = T
    coeff = ${k}
  []
[]

[FVBCs]
  [BC11]
    type = FVSP3ThermalRadiationBC
    boundary = 'left right'
    variable = psi11
    Tb = ${Tb}
    nu = ${nu1}
    nu_low =${nu1}
    nu_high = ${nu2}
    refraction_index = ${n1}
    epsilon = ${epsilon}
    psi = 'psi21'
    order = first
    alpha = ${alpha1}
    beta = ${beta2}
    eta = ${eta1}
  []

  [BC21]
    type = FVSP3ThermalRadiationBC
    boundary = 'left right'
    variable = psi21
    Tb = ${Tb}
    nu = ${nu1}
    nu_low =${nu1}
    nu_high = ${nu2}
    refraction_index = ${n1}
    epsilon = ${epsilon}
    psi = 'psi11'
    order = second
    alpha = ${alpha2}
    beta = ${beta1}
    eta = ${eta2}
  []

  [BC12]
    type = FVSP3ThermalRadiationBC
    boundary = 'left right'
    variable = psi12
    Tb = ${Tb}
    nu = ${nu2}
    nu_low =${nu2}
    nu_high = ${nu3}
    refraction_index = ${n1}
    epsilon = ${epsilon}
    psi = 'psi22'
    order = first
    alpha = ${alpha1}
    beta = ${beta2}
    eta = ${eta1}
  []

  [BC22]
    type = FVSP3ThermalRadiationBC
    boundary = 'left right'
    variable = psi22
    Tb = ${Tb}
    nu = ${nu2}
    nu_low =${nu2}
    nu_high = ${nu3}
    refraction_index = ${n1}
    epsilon = ${epsilon}
    psi = 'psi12'
    order = second
    alpha = ${alpha2}
    beta = ${beta1}
    eta = ${eta2}
  []

  [BC13]
    type = FVSP3ThermalRadiationBC
    boundary = 'left right'
    variable = psi13
    Tb = ${Tb}
    nu = ${nu3}
    nu_low =${nu3}
    nu_high = ${nu4}
    refraction_index = ${n1}
    epsilon = ${epsilon}
    psi = 'psi23'
    order = first
    alpha = ${alpha1}
    beta = ${beta2}
    eta = ${eta1}
  []

  [BC23]
    type = FVSP3ThermalRadiationBC
    boundary = 'left right'
    variable = psi23
    Tb = ${Tb}
    nu = ${nu3}
    nu_low =${nu3}
    nu_high = ${nu4}
    refraction_index = ${n1}
    epsilon = ${epsilon}
    psi = 'psi13'
    order = second
    alpha = ${alpha2}
    beta = ${beta1}
    eta = ${eta2}
  []

  [BC_temperature]
    type = FVSP3TemperatureBC
    boundary = 'left right'
    variable = T
    Tb = ${Tb}
    n1 = ${n1}
    n2 = ${n2}
    h = ${h}
    k = ${k}
    epsilon = ${epsilon}
    alpha = ${alpha}
    nu1 = ${nu1}
    nu_min = ${nu_min}
  []
[]

# [VectorPostprocessors]
#   [y0]
#     num_points = 102
#     start_point = '-0.5 0.0 0.0'
#     end_point = '0.5 0.0 0.0'
#     sort_by = 'x'
#     variable = T
#     type = LineValueSampler
#   []
# []

[Executioner]
  type = Transient
  solve_type = 'Newton'
  petsc_options_iname = '-pc_type -pc_hypre_type -ksp_gmres_restart'
  petsc_options_value = 'hypre boomeramg 500'

  nl_rel_tol = 1e-6
  nl_abs_tol = 1e-6
  l_tol = 1e-6

  l_max_its = 2000
  nl_max_its = 500

  start_time = 0.0
  dt = ${dt}
  end_time = ${endt}
[]

[Outputs]
  [e]
    type = Exodus
    # exodus = true
  []
  [csv]
    type = CSV
    # csv = true
    execute_on = final
  []
[]
