
"use strict";

let MasterboardDataMsg = require('./MasterboardDataMsg.js');
let Analog = require('./Analog.js');
let Digital = require('./Digital.js');
let IOStates = require('./IOStates.js');
let ToolDataMsg = require('./ToolDataMsg.js');
let RobotStateRTMsg = require('./RobotStateRTMsg.js');
let RobotModeDataMsg = require('./RobotModeDataMsg.js');

module.exports = {
  MasterboardDataMsg: MasterboardDataMsg,
  Analog: Analog,
  Digital: Digital,
  IOStates: IOStates,
  ToolDataMsg: ToolDataMsg,
  RobotStateRTMsg: RobotStateRTMsg,
  RobotModeDataMsg: RobotModeDataMsg,
};
