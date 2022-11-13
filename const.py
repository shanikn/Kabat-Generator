
_t0 = 50000.0
t0 = _t0
tstart_ave1 = 1
tstart_ave2 = 10
tstart_ae1 = 5
tstart_ae2 = 10
tstart_fve1 = 9
tstart_fve2 = 14
tstart_fv1 = 1
tstart_fv2 = 13
tstart_turn1 = 1
tstart_turn2 = 5
tend_ave1 = 1
tend_ave2 = 5
tend_ae1 = 9
tend_ae2 = 13
tend_fve1 = 11
tend_fve2 = 14
tend_fv1 = 15
tend_fv2 = 20
azimuth_1 = 10
azimuth_2 = 50
error_max1 = 1000
error_max2 = 1002

ERROR_NAMES_WEIGHTS = [1,1,1,1]
ERROR_AMOUNT_WEIGHTS = [10,10,8,8,5,5,2,1,1,1]

t_start_ave = (tstart_ave1, tstart_ave2)
t_start_ae = (tstart_ae1, tstart_ae2)
t_start_fve = (tstart_fve1, tstart_fve2)
t_start_fv = (tstart_fv1, tstart_fv2)
t_start_turn = (tstart_turn1, tstart_turn2)
t_end_ave = (tend_ave1, tend_ave2)
t_end_ae = (tend_ae1, tend_ae2)
t_end_fve = (tend_fve1, tend_fve2)
t_end_fv = (tend_fv1, tend_fv2)
azimuth = (azimuth_1, azimuth_2)
error_max_ = (error_max1, error_max2)

ERROR_PARAMETERS = [t_start_ave, t_start_ae, t_start_fve, t_start_fv, t_start_turn,
                    t_end_ave, t_end_ae, t_end_fve, t_end_fv, azimuth, error_max_]

TRAJ_PATH = ... #PATH
SCENARIO_PATH = ... #PATH
MEASUREMENTS = ('OPT' 'GPS', 'RDR', 'IMU')
ERRORS = ['AVE', 'AE', 'FVE', 'FV']
