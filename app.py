#!/usr/bin/env python3
import os

import aws_cdk as cdk

from test.test_stack import TestStack

# Use the environment variables if available, otherwise use the default account/region
env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION")
)

app = cdk.App()

TestStack(app, "TestStack", env=env)

app.synth()
