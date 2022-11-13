import numpy as np


def add_vel_error(data, error_max, t0, tstart, tend):
    sig_vel_accuracy = error_max / 30
    data.set_index("ComputerTimeGpsSec")
    index_list = list(data.loc[(data["ComputerTimeGpsSec"]-t0 >= tstart) & (data["ComputerTimeGpsSec"]-t0 <tend)].index)

    for i in index_list:
        #Picks random numbers to add to the original vel
        data.loc[i, "Telemetry.Vx"] += np.random.normal(0, sig_vel_accuracy)
        data.loc[i, "Telemetry.Vy"] += np.random.normal(0, sig_vel_accuracy)
        data.loc[i, "Telemetry.Vz"] += np.random.normal(0, sig_vel_accuracy * 2)

    return data

def add_error(data, error_max, t0, tstart, tend):
    sig_location_accuracy = error_max / 3
    sig_vel_accuracy = error_max / 30
    data.set_index("ComputerTimeGpsSec")
    index_list = list(data.loc[(data["ComputerTimeGpsSec"]-t0 >= tstart) & (data["ComputerTimeGpsSec"]-t0 <tend)].index)

    for i in index_list:
        #Picks random numbers to add to the original vel
        data.loc[i, "Target.Easting"] += np.random.normal(0, sig_vel_accuracy)
        data.loc[i, "Target.Northing"] += np.random.normal(0, sig_vel_accuracy)
        data.loc[i, "Target.Height"] += np.random.normal(0, sig_vel_accuracy * 2)

        data.loc[i, "Telemetry.Vx"] += np.random.normal(0, sig_vel_accuracy)
        data.loc[i, "Telemetry.Vy"] += np.random.normal(0, sig_vel_accuracy)
        data.loc[i, "Telemetry.Vz"] += np.random.normal(0, sig_vel_accuracy * 2)

    return data

def jump(data, t0, string_of_parameters):
    parameters_list = string_of_parameters.split(';')
    fv = []
    for i in parameters_list:
        cell = i.split(',')
        for n in range(len(cell)):
            fv.append(int(cell[(n)]))

        for tstart, tend in fv:
            false_validity(data, t0, tstart, tend)

def false_validity(data, t0, tstart, tend):
    data.loc[(data["ComputerTimeGpsSec"]- t0 >= tstart) & (data["ComputerTimeGpsSec"]- t0 < tend), "validity"] = "FALSE"
    return data

def false_validity_with_error(data, t0, tstart, tend, error1, error2):
    df = add_error(data, error1, t0, tstart-2, tstart-1)
    df2 = add_error(df, error2, t0, tstart-1, tstart)
    final_data = false_validity(df2, t0, tstart, tend)
    return final_data


def turn(data, t0, tstart, azimuth):
    indexes = data[(data["ComputerTimeGpsSec"]-t0 >=tstart)].index
    index_list = list(indexes)

    E = data["Target.Easting"][index_list]
    N = data["Target.Northing"][index_list]
    H = data["Target.Height"][index_list]
    VE = data["TelemetryData.Vx"][index_list]
    VN = data["TelemetryData.Vy"][index_list]
    VH = data["TelemetryData.Vz"][index_list]

    temp_VE = VE
    temp_VN = VN


    delta_x = []
    delta_y = []
    for i in index_list:
        print(i)
        delta_x.append(N[i] - N[i-1])
        delta_y.append(E[i] - E[i - 1])
    for i in range(len(index_list)):
        print(i)
        E[i] =E[i-1] + delta_x[i] * np.sin(azimuth) + delta_y[i] * np.cos(azimuth)
        N[i] = N[i - 1] + delta_x[i] * np.cos(azimuth) + delta_y[i] * np.sin(azimuth)

    data.loc[index_list, "Target.Easting"] = E
    data.loc[index_list, "Target.Northing"] = N
    data.loc[index_list, "Target.Height"] = H
    data.loc[index_list, "TelemetryData.Vx"] = VE
    data.loc[index_list, "TelemetryData.Vy"] = VN
    data.loc[index_list, "TelemetryData.Vz"] = VH

    return data






































