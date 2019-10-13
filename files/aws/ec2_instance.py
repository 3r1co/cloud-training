from troposphere import FindInMap, GetAtt, ImportValue
from troposphere import Output, Ref, Template
from troposphere.ec2 import Tags
from troposphere.autoscaling import LaunchConfiguration,  AutoScalingGroup, Tag as AutoScalingTag

import troposphere.ec2 as ec2

template = Template()

template.add_mapping('RegionMap', {
    "us-east-1": {"AMI": "ami-06e619a8d6b783fa3"},
    "eu-west-1": {"AMI": "ami-089a2a65371000190"},
    "ap-southeast-1": {"AMI": "ami-0e95b2e151e62f64c"}
})

lc = template.add_resource(LaunchConfiguration(
    "Ec2Instance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    SecurityGroups=[ImportValue("prgtrn-SSHSecurityGroupID")],
    IamInstanceProfile=ImportValue("prgtrn-EC2GlobalRole")
))

template.add_resource(AutoScalingGroup(  
        "myASG",  
        AutoScalingGroupName="asg-ibs-d-ew1-prgtrn-emuellen",   
        DesiredCapacity="1", 
        MinSize=1, 
        MaxSize=1,
        VPCZoneIdentifier=[ImportValue("prgtrn-PrivateSubnetAZa1Id"), ImportValue("prgtrn-PrivateSubnetAZb1Id"), ImportValue("prgtrn-PrivateSubnetAZc1Id")],  
        LaunchConfigurationName=Ref(lc),   
        Tags=[AutoScalingTag('gto:finops:projectcode', "R0S28973", True), AutoScalingTag('Name', "asg-ibs-d-ew1-prgtrn-emuellen", True)],
        HealthCheckGracePeriod=300,
        HealthCheckType="ELB"
    )) 

print(template.to_yaml())
