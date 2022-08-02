#!/usr/bin/env python3

import aws_cdk as cdk

from appstream_fleet_bastionhost.appstream_fleet_bastionhost_stack import AppStreamFleetBastionHostStack


app = cdk.App()
AppStreamFleetBastionHostStack(app, "appstream_fleet_bastionhost")

app.synth()
