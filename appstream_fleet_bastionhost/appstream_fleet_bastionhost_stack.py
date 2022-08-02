from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_s3 as s3,
    aws_servicecatalog as sc
)

class AppStreamFleetBastionHostStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "AppStreamFleetBastionHostWorkshopQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "AppStreamFleetBastionHostWorkshopTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))
        
        tag_options = sc.TagOptions(self, 'TagOptions', allowed_values_for_tags = scope.node.try_get_context("tag_options"))

        infra_portfolio = sc.Portfolio(self, 'AppStream Portfolio',
            display_name='AppStream Portfolio',
            description='Potfolio with approved list of AppStream products',
            provider_name='IT Team',
            tag_options=tag_options
        )
        
        product_from_template = sc.CloudFormationProduct(self, 'Product',
            product_name='Elastic AppStream Fleet Product',
            owner='Admin',
            description='Elastic AppStream Fleet Product',
            distributor='ADMIN',
            product_versions = [sc.CloudFormationProductVersion(
                product_version_name="1.0",
                cloud_formation_template=sc.CloudFormationTemplate.from_asset('PATH_TO_YOUR_YAML_FILE')
            )]
        )
        
        infra_portfolio.add_product(product_from_template)
        
        appstream_role = iam.Role(self, 'ROLE_NAME',role_name= 'ROLE_NAME', assumed_by=iam.ServicePrincipal('servicecatalog.amazonaws.com'))
        infra_portfolio.set_local_launch_role(product_from_template, appstream_role, description='Launch Constraint role for AppStream')
        
        infra_portfolio.share_with_account('ACCOUNT_NUMBER')
