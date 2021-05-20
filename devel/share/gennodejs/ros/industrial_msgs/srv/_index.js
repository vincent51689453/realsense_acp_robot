
"use strict";

let SetRemoteLoggerLevel = require('./SetRemoteLoggerLevel.js')
let StopMotion = require('./StopMotion.js')
let StartMotion = require('./StartMotion.js')
let CmdJointTrajectory = require('./CmdJointTrajectory.js')
let GetRobotInfo = require('./GetRobotInfo.js')
let SetDrivePower = require('./SetDrivePower.js')

module.exports = {
  SetRemoteLoggerLevel: SetRemoteLoggerLevel,
  StopMotion: StopMotion,
  StartMotion: StartMotion,
  CmdJointTrajectory: CmdJointTrajectory,
  GetRobotInfo: GetRobotInfo,
  SetDrivePower: SetDrivePower,
};
