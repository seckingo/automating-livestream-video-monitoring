#!/usr/bin/env python
import sys
import boto3
from jinja2 import Environment, FileSystemLoader, select_autoescape

args = 'broadcast-monitoring-VideoProcessingStack-1HD7OSWTPJ3F1'

if not args:
    raise Exception('Name of video-processing stack missing.')


# updates to address security concerns of autoescaping
# see "Notes on Autoescaping" https://jinja.palletsprojects.com/en/3.0.x/api/#basics
jinjaEnv = Environment(loader=FileSystemLoader('./'),
                       autoescape=select_autoescape())

cfn_client = boto3.client('cloudformation')
stack_name = args

response = cfn_client.describe_stacks(StackName=stack_name)["Stacks"]

if not response:
    raise ValueError(f"Could not find CloudFormation {stack_name} in the account.")

cfn_outputs = response[0]['Outputs']
cfn_output_map = {o['OutputKey']: o['OutputValue'] for o in cfn_outputs}
print(cfn_output_map)

file_list = ["amplify/backend/storage/s38b7e1c53/parameters.json.template",
             ".env.template"]

for file_path in file_list:
    jTemplate = jinjaEnv.get_template(file_path)
    new_path = file_path[:file_path.index('.template')]
    output = jTemplate.render(cfn_output_map)
    with open(new_path, 'w') as f:
        f.write(output)
    print(f'Generated {new_path} from template')
