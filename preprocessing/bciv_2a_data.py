import mat2py as mp
from mat2py.core import *


def getData(subject_index):
    subject_index = 6
    session_type = "T"
    dir_1 = M[["D:\MI\BCICIV_2a_gdf\A0", num2str(subject_index), session_type, ".gdf"]]
    s, HDR = sload(dir_1)
    labeldir_1 = M[
        ["D:\MI\true_labels\A0", num2str(subject_index), session_type, ".mat"]
    ]
    load(labeldir_1)
    label_1 = copy(classlabel)
    Pos = HDR.EVENT.POS
    Typ = HDR.EVENT.TYP
    k = 0
    data_1 = zeros(1000, 22, 288)
    for j in M[1 : length(Typ)]:
        if Typ(j) == 768:
            k = k + 1
            data_1[I[:, :, k]] = s(M[(Pos(j) + 500) : (Pos(j) + 1499)], M[1:22])

    data_1[I[isnan(data_1)]] = 0
    session_type = "E"
    dir_2 = M[
        ["D:\Lab\MI\BCICIV_2a_gdf\A0", num2str(subject_index), session_type, ".gdf"]
    ]
    s, HDR = sload(dir_2)
    labeldir_2 = M[
        ["D:\Lab\MI\true_labels\A0", num2str(subject_index), session_type, ".mat"]
    ]
    load(labeldir_2)
    label_2 = copy(classlabel)
    Pos = HDR.EVENT.POS
    Typ = HDR.EVENT.TYP
    k = 0
    data_2 = zeros(1000, 22, 288)
    for j in M[1 : length(Typ)]:
        if Typ(j) == 768:
            k = k + 1
            data_2[I[:, :, k]] = s(M[(Pos(j) + 500) : (Pos(j) + 1499)], M[1:22])

    data_2[I[isnan(data_2)]] = 0
    fc = 250
    Wl = 4
    Wh = 40
    Wn = mrdivide(M[[Wl * 2, Wh * 2]], fc)
    b, a = cheby2(6, 60, Wn)
    for j in M[1:288]:
        data_1[I[:, :, j]] = filtfilt(b, a, data_1[I[:, :, j]])
        data_2[I[:, :, j]] = filtfilt(b, a, data_2[I[:, :, j]])

    data = copy(data_1)
    label = copy(label_1)
    saveDir = M[["D:\MI\standard_2a_data\A0", num2str(subject_index), "T.mat"]]
    save(saveDir, "data", "label")
    data = copy(data_2)
    label = copy(label_2)
    saveDir = M[["D:\MI\standard_2a_data\A0", num2str(subject_index), "E.mat"]]
    save(saveDir, "data", "label")
    return data