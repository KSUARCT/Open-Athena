#!/usr/bin/env python3

import depthai as dai
import numpy as np
import sys
from pathlib import Path

# Connect Device
with dai.Device() as device:
    calibFile = str((Path(__file__).parent / Path(f"calib_{device.getMxId()}.json")).resolve().absolute())
    if len(sys.argv) > 1:
        calibFile = sys.argv[1]

    calibData = device.readCalibration()
    calibData.eepromToJsonFile(calibFile)

    M_rgb, width, height = calibData.getDefaultIntrinsics(dai.CameraBoardSocket.CAM_A)
    print("RGB Camera Default intrinsics...")
    print(M_rgb)
    print(width)
    print(height)
    M_rgb = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.CAM_A, 1280, 720))
    print("RGB Camera resized intrinsics...")
    print(M_rgb)

    D_rgb = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.CAM_A))
    print("RGB Distortion Coefficients...")
    [print(name + ": " + value) for (name, value) in
    zip(["k1", "k2", "p1", "p2", "k3", "k4", "k5", "k6", "s1", "s2", "s3", "s4", "τx", "τy"],
    [str(data) for data in D_rgb])]

    print(f'RGB FOV {calibData.getFov(dai.CameraBoardSocket.CAM_A)}')
