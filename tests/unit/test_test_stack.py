import os

import aws_cdk as cdk
import aws_cdk.assertions as assertions

from test.test_stack import TestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in test/test_stack.py
def test_sqs_queue_created():
    # Use the environment variables if available, otherwise use the default account/region
    env = cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION")
    )

    app = cdk.App()
    stack = TestStack(app, "test", env=env)
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
