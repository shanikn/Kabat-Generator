import datetime

import utm
import random
import pandas as pd
import os
from const import *
from errors import *


def create_final_format(traj, kind):
    kind_dict = {'OPT': (0, 'OPT', 3, 0), 'RDR': (1, 'RDR', 4, 1), 'GPS': (2, 'GPS', 5, 2), 'IMU': (3, 'IMU', 5, 3)}

    parent_id, name, accuracy_score, ip = kind_dict[f"{kind}"]

    traj = pd.read_csv(traj)

    final_data = pd.DataFrame()

    E = traj["E"]
    N = traj["N"]
    H = traj["H"]
    VE = traj["VE"]
    VN = traj["VN"]
    VH = traj["VH"]

    lat, lon = utm.to_latlon(E, N, 36, 'R')

    time = traj.get("TIME") + t0
    ComputerTime = []
    for i in range(len(time)):
        val = datetime.datetime(2022, 11, 24, 12, 15, 55, 3423) + datetime.timedelta(seconds=traj.get("Time")[i])
        ComputerTime.append(val.strftime('%H:%M:%S.%F'))

    final_data['ComputerTime'] = ComputerTime
    final_data['ComputerTimeGpsSec'] = time
    final_data['TriggerTimeGPS'] = time[0]
    final_data['TelemetryData.HeaderLength'] = 11
    final_data['TelemetryData.MessageType'] = 30
    final_data['TelemetryData.MessageTime'] = 7255122
    final_data['TelemetryData.MessageLength'] = 66
    final_data['TelemetryData.MessageCounter'] = 32574
    final_data['TelemetryData.ObjectID'] = 195
    final_data['TelemetryData.SlavingValidity'] = 1
    final_data['TelemetryData.SlavingTime'] = 7255
    final_data['TelemetryData.Lat'] = lat
    final_data['TelemetryData.Lon'] = lon
    final_data['TelemetryData.Alt'] = H
    final_data['TelemetryData.Vx'] = VE
    final_data['TelemetryData.Vy'] = VN
    final_data['TelemetryData.Vz'] = VH
    final_data['TelemetryData.Checksum'] = 54
    final_data['ReceiveFromClientPort'] = 6013
    final_data['ParentID'] = ParentID
    final_data['Validity'] = 'TRUE'
    final_data['AccuracyScore'] = accuracy_score
    final_data['Target.Easting'] = E
    final_data['Target.Northing'] = N
    final_data['Target.Height'] = H
    final_data['Target.Name'] = 'Spirit_May21'
    final_data['Icd'] = 'MalamTelemetry'
    final_data['Location.Easting'] = 680144.0607
    final_data['Location.Northing'] = 3325143.018
    final_data['Location.Height'] = 548.1953727
    final_data['Location.Name'] = name
    final_data['ClientType'] = 'MalamTelemetry'
    final_data['ClientId'] = parent_id
    final_data['Name'] = name
    final_data['IsAlive'] = 'TRUE'
    final_data['IpEndPoint'] = '192.168.0.12' + str(ip) + ":4001"

    return final_data

def get_random_file(): #tuple
    random_file_names = []
    for x in range(4):
        random_file_names.append(random.choice(os.listdir(TRAJ_PATH)))
    return tuple(random_file_names)

def get_amount_of_errors():
    errors_amount_list = random.choices(range(0, 10), weights=ERROR_AMOUNT_WEIGHTS, k=1)#How manyerrors will accure to each measurement
    errors_amount = errors_amount_list[0]
    return errors_amount

def get_errors_names(amount):
    error_choices = []
    for i in range(amount):
        error_choice = random.choices(ERRORS, weights=ERROR_NAMES_WEIGHTS)
        error_choice = error_choice[0]
        error_choices.append(error_choice)
    return error_choices

def save_file_by_measurement(measurement_dict, scenario_number, new_name):
    path=SCENARIO_PATH
    os.makedirs(path + f"/{new_name}//Scenario {scenario_number}")
    for df_key. df in measurement_dict.items():
        df.to_csv(path + f"//{new_name}//Scenario {scenario_number}//Final Format {df_key}.csv", index=False)

def get_txt_documantation(location, new_name, number_of_scenario=None, measurement=None, errors_representation=None):
    with open(f"{SCENARIO_PATH}//Projects Documantation//Scenario_Information {new_name}.txt", mode='a') as f:
        if location == 'first':
            f.write("Scenario Information:\n")
        elif location == 'second':
            f.write(f"\n------------------------------------------------"
                    f"--------------------------------------------------\nScenario Number {number_of_scenario}\n")
        elif location == 'third':
            f.write(f"{measurement} has -> {errors_representation}\n")


def get_errors():
    aomunt = get_amount_of_errors()
    error_choices = get_errors_names(amount)
    return error_choices

def apply_errors(error_list, measurement_dict, measurement, **kwargs):
    erros_representation = []
    if 'FV' in error_list:
        measurement_dict[measurement] = false_validity(measurement_dict[measurement], t0, kwargs['tstart_fv'], kwargs['tend_fv'])
        erros_representation.append("FV: {:.lf} until {:.lf}".format(kwargs['tstart_fv'], kwargs['tend_fv']))
    if 'AVE' in error_list:
        measurement_dict[measurement] = add_vel_error(measurement_dict[measurement], kwargs['error_max'],  t0, kwargs['tstart_ave'],
                                                       kwargs['tend_ave'])
        erros_representation.append("AVE: {:.lf} until {:.lf}".format(kwargs['tstart_ave'], kwargs['tend_ave']))
    if 'AE' in error_list:
        measurement_dict[measurement] = add_error(measurement_dict[measurement], kwargs['error_max'], t0, kwargs['tstart_ae'],
                                                       kwargs['tend_ae'])
        erros_representation.append("AE: {:.lf} until {:.lf}".format(kwargs['tstart_ae'], kwargs['tend_ae']))
    if 'FVE' in error_list:
        measurement_dict[measurement] = false_validity_with_error(measurement_dict[measurement], t0, kwargs['tstart_fve'],
                                                       kwargs['tend_fve'], error_max1, error_max2)
        erros_representation.append("FVE: {:.lf} until {:.lf}".format(kwargs['tstart_fve'], kwargs['tend_fve']))
    if 'TURN' in error_list:
        measurement_dict[measurement] = turn(measurement_dict[measurement], t0, kwargs['tstart_turn'], kwargs['azimuth'])
        erros_representation.append("Turn: {:.lf} until {:.2f}".format(kwargs['tstart_turn'], kwargs['azimuth']))
    return measurement_dict[measurement], erros_representation


def get_parameter_list():
    parameters_list = []
    for error in ERROR_PARAMETERS:
        parameters_list.append(random.uniform(error[0], error[1]))
    return parameters_list
















