from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class TestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Example SQS Queue
        queue = sqs.Queue(
             self, "TestQueue",
             visibility_timeout=Duration.seconds(300),
        )

        # Example EC2 instance
        ec2_instance = ec2.Instance(
            self, "MyInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=ec2.Vpc.from_lookup(self, "VPC", is_default=True),
        )

        CfnOutput(
            self, "QueueURL",
            value=queue.queue_url,
            description="URL of the SQS queue",
        )
        CfnOutput(
            self, "InstanceID",
            value=ec2_instance.instance_id,
            description="ID of the EC2 instance",
        )