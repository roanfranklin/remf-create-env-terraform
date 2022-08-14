#!/usr/bin/python3
#
# ..:: REMF Scritps - IaC Terraform ::..
#
# by: Roan Franklin (https://github.com/roanfranklin)
# start date: 04 Julho de 2022
# 
# Criação de arquivos ambientes Terraform para AWS.
#

import sys
import os
import argparse
import glob
import yaml

# ###################################################################################################
# FUNÇÕES E PROCEDIMENTOS PADRÕES DO SISTEMA
def logoCloudOpss(SCRIPT, BY, DATE, DESC):
  LOGO = '''
..:: {0} - https://remf.com.br/ ::..

Descrição: {3}
'''.format(SCRIPT, BY, DATE, DESC)
  print(LOGO)

def logoREMF():
  LOGO = '''
# ################################################
#
# RoaNFRaNKLiN
# https://github.com/roanfranklin
#
# ################################################
'''
  print(LOGO)

def question(QUESTION):
  print(' {0}?'.format(QUESTION))
  CONFIRM = input('\n Confirmar ( YES | no ) # ')
  if any(CONFIRM.lower() == OP for OP in ['yes', 'ye', 'y', 'sim', 'si', 's', '1']):
    return True
  elif any(CONFIRM.lower() == OP for OP in ['no', 'n', 'nao', 'na', 'n', 'não', 'nã', '0']):
    return False
  else:
    return True


def output(STATUS='*', MSG='', START=False, END=False):
  if START:
    print('')
  print('[ {0} ] {1}'.format(STATUS, MSG))
  if END:
    print('')


def output_service(MSG=''):
  print('')
  print('# ################################################')
  print('# {0}'.format(MSG))
  print('')


def dirExist(DIR):
  isExist = os.path.exists(DIR)
  if not isExist:
    os.makedirs(DIR)
    output('+', 'Criado o diretório "{0}".'.format(DIR))


def writefile(TYPE, FILE, DATA):
  try:
    f = open(FILE, TYPE)
    f.write(DATA)
    f.close()
  except:
    output('!', 'Erro ao criar/modificar o arquivo "{0}".'.format(FILE))
  output('+', 'Sucesso ao criar/modificar o arquivo "{0}".'.format(FILE))


def deletefile(FILE):
  if os.path.exists(FILE):
    os.remove(FILE)
    output('+', 'Sucesso ao deletar o arquivo "{0}".'.format(FILE))
  else:
    output('!', 'Erro ao deletar o arquivo "{0}".'.format(FILE))



# ###################################################################################################
# TEMPLATES DO ARQUIVO YAML

def create_yamlsample(DIR):
  DATA_YAML=open('{0}/sample.yaml'.format(DIR_TEMPLATES_AWS), 'r').read()
  
  FILE_DATA_YAML='{0}/sample.yaml'.format(DIR)
  if question('Deseja criar o arquivo {0}'.format(FILE_DATA_YAML)):
    output_service('Arquivo YAML de amostra/exemplo do seu projeto "{0}"'.format(FILE_DATA_YAML))
    writefile('w', FILE_DATA_YAML, DATA_YAML)
  else:
    output_service('# Exemplo do arquivo que seria criado: \n\n{0}'.format(DATA_YAML))


def create_secrets_tfvars(DIR, FILE_YAML):
  # try:
  config = yaml.safe_load(open('{0}/{1}'.format(DIR, FILE_YAML)))

  PROJECT = config.get('project')
  AWS_ACCOUNT = config.get('aws_account')
  REGION = config.get('region')
  ENV = config.get('environment')
  S3_STATE = config.get('s3_state')

  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'environment': ENV.lower(),
    's3_state': S3_STATE,
    'dir_output_start': DIR
  }

  TEMPLATE_SECRETS_TFVARS = open('{0}/secrets/var_env.tfvars'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

  FILE_SECRETS_TFVARS='{0}/{1}/secrets.tfvars'.format(DIR, ENV.upper())
  writefile('w', FILE_SECRETS_TFVARS, TEMPLATE_SECRETS_TFVARS)

  create_s3state(results)

  SERVICES = config.get('services')
  for service in SERVICES:

    if str(SERVICES[service].get('service')).upper() == 'NETWORK':
      results['network'] = create_network(results,
                                          service,
                                          SERVICES[service])
    elif str(SERVICES[service].get('service')).upper() == 'EKS':
      results['eks'] = create_eks(results,
                                  service,
                                  SERVICES[service])
    elif str(SERVICES[service].get('service')).upper() == 'ECR':
      results['ecr'] = create_ecr(results,
                                  service,
                                  SERVICES[service])
    elif str(SERVICES[service].get('service')).upper() == 'ROUTE53':
      results['route53'] = create_route53(results,
                                  service,
                                  SERVICES[service])
    elif str(SERVICES[service].get('service')).upper() == 'EC2':
      results['ec2'] = create_ec2(results,
                                  service,
                                  SERVICES[service])
  # except:
  #   pass
  


# ###################################################################################################
# TEMPLATES DOS ARQUIVOS TERRAFORM

# Bucket S3
def create_s3state(DATA):
  POSITION = 0
  SERVICE = 'S3-State'
  PROJECT = DATA.get('project')
  AWS_ACCOUNT = DATA.get('aws_aacount')
  REGION = DATA.get('region')
  ENV = DATA.get('environment')
  DIR = DATA.get('dir_output_start')
  S3_STATE = DATA.get('s3_state')
  DIR_OUTPUT = '{0}/{1}/{2:02}-{3}-{1}'.format(DIR, ENV.upper(), POSITION, SERVICE.upper())

  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'env_upper': ENV.upper(),
    'env_lower': ENV.lower(),
    's3_state': S3_STATE,
    'service_upper': SERVICE.upper(),
    'service_lower': SERVICE.lower(),
  }

  TEMPLATE_S3STATE = open('{0}/s3-state/s3.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_DYNAMODB = open('{0}/s3-state/dynamodb.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER = open('{0}/s3-state/provider.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES = open('{0}/s3-state/variables.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

  if S3_STATE == True:
    DIR_S3STATE = DIR_OUTPUT
    output_service('Serviço S3-State no diretório "{0}"'.format(DIR_S3STATE))
    dirExist(DIR_S3STATE)

    FILE_S3STATE='{0}/s3.tf'.format(DIR_S3STATE)
    writefile('w', FILE_S3STATE, TEMPLATE_S3STATE)

    FILE_DYNAMODB='{0}/dynamodb.tf'.format(DIR_S3STATE)
    writefile('w', FILE_DYNAMODB, TEMPLATE_DYNAMODB)

    FILE_PROVIDER='{0}/provider.tf'.format(DIR_S3STATE)
    writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER)

    FILE_VARIABLES='{0}/variables.tf'.format(DIR_S3STATE)
    writefile('w', FILE_VARIABLES, TEMPLATE_VARIABLES)
  else:
    pass


def create_network(OUTPUT_RESULTS, NAME, DATA):
  DIR = OUTPUT_RESULTS.get('dir_output_start')
  PROJECT = OUTPUT_RESULTS.get('project')
  AWS_ACCOUNT = OUTPUT_RESULTS.get('aws_account')
  REGION = OUTPUT_RESULTS.get('region')
  ENV = OUTPUT_RESULTS.get('environment')
  S3_STATE = OUTPUT_RESULTS.get('s3_state')
  SERVICE = DATA.get('service')
  POSITION = DATA.get('position')
  ACTIVE = DATA.get('active')
  if SERVICE.upper() == NAME.upper():
    DIR_OUTPUT = '{0}/{1:02}-{2}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper())
  else:
    DIR_OUTPUT = '{0}/{1:02}-{2}-{3}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper(), NAME.upper())
  CIDR = DATA.get('cidr')
  SUBNETS_PUBLIC = DATA.get('subnets_public')
  SUBNETS_PRIVATE = DATA.get('subnets_private')
  XX = CIDR.split('.')
  CIDR_2OCTETOS = '{0}.{1}'.format(XX[0],XX[1])
  VPC_ENABLE_DNS_HOSTNAMES = DATA.get('vpc_enable_dns_hostnames')
  VPC_ENABLE_DNS_SUPPORT = DATA.get('vpc_enable_dns_support')
  VPC_ASSIGN_GENERATED_IPV6_CIDR_BLOCK = DATA.get('vpc_assign_generated_ipv6_cidr_block')

  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'env_upper': ENV.upper(),
    'env_lower': ENV.lower(),
    's3_state': S3_STATE,
    'service_upper': SERVICE.upper(),
    'service_lower': SERVICE.lower(),
    'active': ACTIVE,    
    'name': NAME,
    'dir_output_network': '{0}/{1}'.format(DIR, DIR_OUTPUT),
    'position': POSITION,
    'cidr_env': CIDR,
    'cidr_2octectos': CIDR_2OCTETOS,
    'subnets_public_total': SUBNETS_PUBLIC,
    'subnets_private_total': SUBNETS_PRIVATE,
    'vpc_enable_dns_hostnames': str(VPC_ENABLE_DNS_HOSTNAMES).lower(),
    'vpc_enable_dns_support': str(VPC_ENABLE_DNS_SUPPORT).lower(),
    'vpc_assign_generated_ipv6_cidr_block': str(VPC_ASSIGN_GENERATED_IPV6_CIDR_BLOCK).lower()
  }

  TEMPLATE_EIP = open('{0}/network/eip.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_IG = open('{0}/network/internetgateway.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_NG = open('{0}/network/natgateway.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_OUTPUT = open('{0}/network/output.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_OUTPUT_END = open('{0}/output_end.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER_S3_STATE = open('{0}/network/provider_s3state.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER = open('{0}/network/provider.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_RT = open('{0}/network/routetable.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_SUBNETS = open('{0}/network/subnets.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES = open('{0}/network/variables.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VPC = open('{0}/network/vpc.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

  if results.get('active') == True:
    DIR_NETWORK = results.get('dir_output_network')
    output_service('Serviço {1} no diretório "{0}"'.format(DIR_NETWORK, SERVICE.upper()))
    dirExist(DIR_NETWORK)

    FILE_EIP='{0}/eip.tf'.format(DIR_NETWORK)
    writefile('w', FILE_EIP, TEMPLATE_EIP)

    FILE_IG='{0}/internetgateway.tf'.format(DIR_NETWORK)
    writefile('w', FILE_IG, TEMPLATE_IG)

    FILE_NG='{0}/natgateway.tf'.format(DIR_NETWORK)
    writefile('w', FILE_NG, TEMPLATE_NG)

    FILE_OUTPUT='{0}/output.tf'.format(DIR_NETWORK)
    writefile('w', FILE_OUTPUT, TEMPLATE_OUTPUT)

    for index, value in enumerate(range(SUBNETS_PRIVATE)):
      output_results = {
        'index': index,
        'az': value+1
      }
      TEMPLATE_OUTPUT_PRIVATE = open('{0}/network/output_subnet_private.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**output_results)
      FILE_OUTPUT='{0}/output.tf'.format(DIR_NETWORK)
      writefile('a', FILE_OUTPUT, TEMPLATE_OUTPUT_PRIVATE)

    for index, value in enumerate(range(SUBNETS_PUBLIC)):
      output_results = {
        'index': index,
        'az': value+1
      }
      TEMPLATE_OUTPUT_PRIVATE = open('{0}/network/output_subnet_public.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**output_results)
      FILE_OUTPUT='{0}/output.tf'.format(DIR_NETWORK)
      writefile('a', FILE_OUTPUT, TEMPLATE_OUTPUT_PRIVATE)

    FILE_OUTPUT='{0}/output.tf'.format(DIR_NETWORK)
    writefile('a', FILE_OUTPUT, TEMPLATE_OUTPUT_END)

    if results.get('s3_state') == True:
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_NETWORK)
      writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER_S3_STATE)
    
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_NETWORK)
      writefile('a', FILE_PROVIDER, TEMPLATE_PROVIDER)
    else:
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_NETWORK)
      writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER)

    FILE_RT='{0}/routetable.tf'.format(DIR_NETWORK)
    writefile('w', FILE_RT, TEMPLATE_RT)

    FILE_SUBNETS='{0}/subnets.tf'.format(DIR_NETWORK)
    writefile('w', FILE_SUBNETS, TEMPLATE_SUBNETS)

    FILE_VARIABLES='{0}/variables.tf'.format(DIR_NETWORK)
    writefile('w', FILE_VARIABLES, TEMPLATE_VARIABLES)

    FILE_VPC='{0}/vpc.tf'.format(DIR_NETWORK)
    writefile('w', FILE_VPC, TEMPLATE_VPC)

    TEMPLATE_SECRETS_TFVARS = open('{0}/secrets/var_network.tfvars'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

    FILE_SECRETS_TFVARS='{0}/{1}/secrets.tfvars'.format(DIR, ENV.upper())
    output_service('Arquivo de Segredos "{0}"'.format(FILE_SECRETS_TFVARS))
    writefile('a', FILE_SECRETS_TFVARS, TEMPLATE_SECRETS_TFVARS)    
  else:
    pass

  return results



def create_eks(OUTPUT_RESULTS, NAME, DATA):
  DIR = OUTPUT_RESULTS.get('dir_output_start')
  PROJECT = OUTPUT_RESULTS.get('project')
  AWS_ACCOUNT = OUTPUT_RESULTS.get('aws_account')
  REGION = OUTPUT_RESULTS.get('region')
  ENV = OUTPUT_RESULTS.get('environment')
  S3_STATE = OUTPUT_RESULTS.get('s3_state')
  SERVICE = DATA.get('service')
  POSITION = DATA.get('position')
  ACTIVE = DATA.get('active')
  if SERVICE.upper() == NAME.upper():
    DIR_OUTPUT = '{0}/{1:02}-{2}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper())
  else:
    DIR_OUTPUT = '{0}/{1:02}-{2}-{3}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper(), NAME.upper())
  WORKER_NODES = DATA.get('worker_nodes')
  WORKER_NODES_INSTANCE_TYPE = WORKER_NODES.get('instance_types')
  NODE_SCALING_CONFIG = DATA.get('node_scaling_config')
  NODE_SCALING_CONFIG_DESIRED_SIZE = NODE_SCALING_CONFIG.get('desired_size')
  NODE_SCALING_CONFIG_MAX_SIZE = NODE_SCALING_CONFIG.get('max_size')
  NODE_SCALING_CONFIG_MIN_SIZE = NODE_SCALING_CONFIG.get('min_size')
  ENCRYPTION_CONFIG = DATA.get('encryption_config')
  ENCRYPTION_CONFIG_RESOURCES = ENCRYPTION_CONFIG.get('resources')
  ENCRYPTION_CONFIG_PROVIDER_KMS = ENCRYPTION_CONFIG.get('provider_kms')
  ENCRYPTION_CONFIG_DELETION_WINDOW_IN_DAYS = ENCRYPTION_CONFIG_PROVIDER_KMS.get('deletion_window_in_days')
  ENCRYPTION_CONFIG_ENABLE_KEY_ROTATION = str(ENCRYPTION_CONFIG_PROVIDER_KMS.get('enable_key_rotation')).lower()

  EKS_AWS_USER = DATA.get('aws_users')
  MAPUSERS = 'mapUsers: |\n'
  for index, USER in enumerate(EKS_AWS_USER):
    MAPUSERS += '''    - userarn: arn:aws:iam::{0}:user/{1}
      username: {1}
      groups:
        - system:masters'''.format(AWS_ACCOUNT, USER)
    if (index + 1) < len(EKS_AWS_USER):
      MAPUSERS += '\n'
    
  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'env_upper': ENV.upper(),
    'env_lower': ENV.lower(),
    's3_state': S3_STATE,
    'service_upper': SERVICE.upper(),
    'service_lower': SERVICE.lower(),
    'position': POSITION,
    'active': ACTIVE,
    'worker_nodes_instance_type': str(WORKER_NODES_INSTANCE_TYPE).replace('\'','"'),
    'node_scaling_desired_size': NODE_SCALING_CONFIG_DESIRED_SIZE,
    'node_scaling_max_size': NODE_SCALING_CONFIG_MAX_SIZE,
    'node_scaling_min_size': NODE_SCALING_CONFIG_MIN_SIZE,
    'encryption_config_resources': str(ENCRYPTION_CONFIG_RESOURCES).replace('\'','"'),
    'encryption_config_provider_kms': ENCRYPTION_CONFIG_PROVIDER_KMS,
    'encryption_config_deletion_window_in_days': ENCRYPTION_CONFIG_DELETION_WINDOW_IN_DAYS,
    'encryption_config_enable_key_rotation': ENCRYPTION_CONFIG_ENABLE_KEY_ROTATION,
    'mapusers': MAPUSERS
  }

  TEMPLATE_EKS_CLUSTER = open('{0}/eks/eks-cluster.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_EKS_NODES = open('{0}/eks/eks-worker-nodes.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_KMS = open('{0}/eks/kms.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_OUTPUT = open('{0}/eks/output.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_OUTPUT += open('{0}/output_end.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER = open('{0}/eks/provider.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER_S3_STATE = open('{0}/eks/provider_s3state.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES = open('{0}/eks/variables.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VPC = open('{0}/eks/vpc.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_EKS_CONFIGMAP_AWS_AUTH_YAML = open('{0}/eks/config/configmap-aws-auth.yaml'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_EKS_ADMIN_SERVICE_ACCOUNT_YAML = open('{0}/eks/config/eks-admin-service-account.yaml'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  
  if results.get('active') == True:
    DIR_EKS = DIR_OUTPUT
    output_service('Serviço {1} no diretório "{0}"'.format(DIR_EKS, SERVICE.upper()))
    dirExist(DIR_EKS)

    FILE_EKS_CLUSTER='{0}/eks-cluster.tf'.format(DIR_EKS)
    writefile('w', FILE_EKS_CLUSTER, TEMPLATE_EKS_CLUSTER)

    FILE_EKS_NODES='{0}/eks-worker-nodes.tf'.format(DIR_EKS)
    writefile('w', FILE_EKS_NODES, TEMPLATE_EKS_NODES)

    FILE_KMS='{0}/kms.tf'.format(DIR_EKS)
    writefile('w', FILE_KMS, TEMPLATE_KMS)

    FILE_OUTPUT='{0}/output.tf'.format(DIR_EKS)
    writefile('w', FILE_OUTPUT, TEMPLATE_OUTPUT)

    if results.get('s3_state') == True:  
      FILE_PROVIDER_S3_STATE='{0}/provider.tf'.format(DIR_EKS)
      writefile('w', FILE_PROVIDER_S3_STATE, TEMPLATE_PROVIDER_S3_STATE)

      FILE_PROVIDER='{0}/provider.tf'.format(DIR_EKS)
      writefile('a', FILE_PROVIDER, TEMPLATE_PROVIDER)      
    else:
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_EKS)
      writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER)

    FILE_VARIABLES='{0}/variables.tf'.format(DIR_EKS)
    writefile('w', FILE_VARIABLES, TEMPLATE_VARIABLES)

    FILE_VPC='{0}/vpc.tf'.format(DIR_EKS)
    writefile('w', FILE_VPC, TEMPLATE_VPC)

    # Create 02-EKS-DEV/config
    DIR_EKS_CONFIG='{0}/config'.format(DIR_EKS)
    dirExist(DIR_EKS_CONFIG)

    FILE_EKS_CONFIGMAP_AWS_AUTH_YAM='{0}/configmap-aws-auth.yaml'.format(DIR_EKS_CONFIG)
    writefile('w', FILE_EKS_CONFIGMAP_AWS_AUTH_YAM, TEMPLATE_EKS_CONFIGMAP_AWS_AUTH_YAML)

    FILE_EKS_ADMIN_SERVICE_ACCOUNT_YAML='{0}/eks-admin-service-account.yaml'.format(DIR_EKS_CONFIG)
    writefile('w', FILE_EKS_ADMIN_SERVICE_ACCOUNT_YAML, TEMPLATE_EKS_ADMIN_SERVICE_ACCOUNT_YAML)

    TEMPLATE_SECRETS_TFVARS = open('{0}/secrets/var_eks.tfvars'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

    FILE_SECRETS_TFVARS='{0}/{1}/secrets.tfvars'.format(DIR, ENV.upper())
    output_service('Arquivo de Segredos "{0}"'.format(FILE_SECRETS_TFVARS))
    writefile('a', FILE_SECRETS_TFVARS, TEMPLATE_SECRETS_TFVARS)
  else:
    pass

  return results


def create_ecr(OUTPUT_RESULTS, NAME, DATA):
  DIR = OUTPUT_RESULTS.get('dir_output_start')
  PROJECT = OUTPUT_RESULTS.get('project')
  AWS_ACCOUNT = OUTPUT_RESULTS.get('aws_account')
  REGION = OUTPUT_RESULTS.get('region')
  ENV = OUTPUT_RESULTS.get('environment')
  S3_STATE = OUTPUT_RESULTS.get('s3_state')
  SERVICE = DATA.get('service')
  POSITION = DATA.get('position')
  ACTIVE = DATA.get('active')
  if SERVICE.upper() == NAME.upper():
    DIR_OUTPUT = '{0}/{1:02}-{2}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper())
  else:
    DIR_OUTPUT = '{0}/{1:02}-{2}-{3}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper(), NAME.upper())
  REPOSITORIES = DATA.get('repositories')
  VALUE = []
  TEMPLATE_ECR = ''
  for repository in REPOSITORIES:
    if REPOSITORIES[repository].get('active') == True:
      IMAGE_SCANNING = REPOSITORIES[repository].get('image_scanning')
      XX = {
        'name': repository ,
        'image_tag_mutability': str(REPOSITORIES[repository].get('image_tag_mutability')).upper(),
        'image_scan_on_push': str(IMAGE_SCANNING.get('scan_on_push')).lower(),
      }
      VALUE.append(XX)

    TEMPLATE_ECR += open('{0}/ecr/ecr.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**XX)

  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'env_upper': ENV.upper(),
    'env_lower': ENV.lower(),
    's3_state': S3_STATE,
    'service_upper': SERVICE.upper(),
    'service_lower': SERVICE.lower(),
    'position': POSITION,
    'active': ACTIVE,
    'repositories': VALUE
  }

  TEMPLATE_PROVIDER = open('{0}/ecr/provider.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(*results)
  TEMPLATE_PROVIDER_S3_STATE = open('{0}/ecr/provider_s3state.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES =  open('{0}/ecr/variables.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

  if results.get('active') == True:
    DIR_ECR = DIR_OUTPUT
    output_service('Serviço {1} no diretório "{0}"'.format(DIR_ECR, SERVICE.upper()))
    dirExist(DIR_ECR)

    FILE_ECR='{0}/ecr.tf'.format(DIR_ECR)
    writefile('w', FILE_ECR, TEMPLATE_ECR)

    if results.get('s3_state') == True:
      FILE_PROVIDER_S3_STATE='{0}/provider.tf'.format(DIR_ECR)
      writefile('w', FILE_PROVIDER_S3_STATE, TEMPLATE_PROVIDER_S3_STATE)
      
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_ECR)
      writefile('a', FILE_PROVIDER, TEMPLATE_PROVIDER)
    else:
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_ECR)
      writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER)

    FILE_VARIABLES='{0}/variables.tf'.format(DIR_ECR)
    writefile('w', FILE_VARIABLES, TEMPLATE_VARIABLES)

    TEMPLATE_SECRETS_TFVARS = open('{0}/secrets/var_ecr.tfvars'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

    FILE_SECRETS_TFVARS='{0}/{1}/secrets.tfvars'.format(DIR, ENV.upper())
    output_service('Arquivo de Segredos "{0}"'.format(FILE_SECRETS_TFVARS))
    writefile('a', FILE_SECRETS_TFVARS, TEMPLATE_SECRETS_TFVARS)
  else:
    pass

  return results


def create_route53(OUTPUT_RESULTS, NAME, DATA):
  DIR = OUTPUT_RESULTS.get('dir_output_start')
  PROJECT = OUTPUT_RESULTS.get('project')
  AWS_ACCOUNT = OUTPUT_RESULTS.get('aws_account')
  REGION = OUTPUT_RESULTS.get('region')
  ENV = OUTPUT_RESULTS.get('environment')
  S3_STATE = OUTPUT_RESULTS.get('s3_state')
  SERVICE = DATA.get('service')
  POSITION = DATA.get('position')
  ACTIVE = DATA.get('active')
  if SERVICE.upper() == NAME.upper():
    DIR_OUTPUT = '{0}/{1:02}-{2}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper())
  else:
    DIR_OUTPUT = '{0}/{1:02}-{2}-{3}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper(), NAME.upper())
  RECORDS = DATA.get('record')
  DOMAIN = DATA.get('domain')
  VALUE = []

  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'env_upper': ENV.upper(),
    'env_lower': ENV.lower(),
    's3_state': S3_STATE,
    'service_upper': SERVICE.upper(),
    'service_lower': SERVICE.lower(),
    'position': POSITION,
    'active': ACTIVE,
    'domain': DOMAIN
  }

  TEMPLATE_ROUTE53 = open('{0}/route53/route53.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  
  for record in RECORDS:
    if RECORDS[record].get('active') == True:
      WEIGHTED_ROUTING_POLICY = RECORDS[record].get('weighted_routing_policy')

      if WEIGHTED_ROUTING_POLICY is None:
        WEIGHTED_ROUTING_POLICY = 0
      else:
        WEIGHTED_ROUTING_POLICY = WEIGHTED_ROUTING_POLICY.get('weight')

      XX = {
        'domain': DOMAIN,
        'record_name': record,
        'type': RECORDS[record].get('type'),
        'records': RECORDS[record].get('records'),
        'ttl': RECORDS[record].get('ttl'),
        'weighted_routing_policy_weight': WEIGHTED_ROUTING_POLICY,
        'alias_name': RECORDS[record].get('name'),
        'alias_zone_id': RECORDS[record].get('zone_id'),
        'alias_evaluate_target_health': str(RECORDS[record].get('evaluate_target_health')).lower()
      }
      VALUE.append(XX)

      if XX.get('type') == 'a':
        TEMPLATE_ROUTE53 += open('{0}/route53/route53_arecord.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**XX)
      elif XX.get('type') == 'alias':
        TEMPLATE_ROUTE53 += open('{0}/route53/route53_aliasrecord.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**XX)
      elif XX.get('type') == 'cname':
        TEMPLATE_ROUTE53 += open('{0}/route53/route53_cnamerecord.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**XX)

  # TEMPLATE_ROUTE53 += open('{0}/route53/route53.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_OUTPUT =  open('{0}/route53/output.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_OUTPUT += open('{0}/output_end.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER = open('{0}/route53/provider.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER_S3_STATE = open('{0}/route53/provider_s3state.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES =  open('{0}/route53/variables.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

  if results.get('active') == True:
    DIR_ROUTE53 = DIR_OUTPUT
    output_service('Serviço {1} no diretório "{0}"'.format(DIR_ROUTE53, SERVICE.upper()))
    dirExist(DIR_ROUTE53)

    FILE_ROUTE53='{0}/route53.tf'.format(DIR_ROUTE53)
    writefile('w', FILE_ROUTE53, TEMPLATE_ROUTE53.replace('root.','').replace('\'','"'))

    FILE_OUTPUT='{0}/output.tf'.format(DIR_ROUTE53)
    writefile('w', FILE_OUTPUT, TEMPLATE_OUTPUT)

    if results.get('s3_state') == True:
      FILE_PROVIDER_S3_STATE='{0}/provider.tf'.format(DIR_ROUTE53)
      writefile('w', FILE_PROVIDER_S3_STATE, TEMPLATE_PROVIDER_S3_STATE)
      
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_ROUTE53)
      writefile('a', FILE_PROVIDER, TEMPLATE_PROVIDER)
    else:
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_ROUTE53)
      writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER)

    FILE_VARIABLES='{0}/variables.tf'.format(DIR_ROUTE53)
    writefile('w', FILE_VARIABLES, TEMPLATE_VARIABLES)

    TEMPLATE_SECRETS_TFVARS = open('{0}/secrets/var_route53.tfvars'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

    FILE_SECRETS_TFVARS='{0}/{1}/secrets.tfvars'.format(DIR, ENV.upper())
    output_service('Arquivo de Segredos "{0}"'.format(FILE_SECRETS_TFVARS))
    writefile('a', FILE_SECRETS_TFVARS, TEMPLATE_SECRETS_TFVARS)
  else:
    pass

  return results


def create_ec2(OUTPUT_RESULTS, NAME, DATA):
  DIR = OUTPUT_RESULTS.get('dir_output_start')
  PROJECT = OUTPUT_RESULTS.get('project')
  AWS_ACCOUNT = OUTPUT_RESULTS.get('aws_account')
  REGION = OUTPUT_RESULTS.get('region')
  ENV = OUTPUT_RESULTS.get('environment')
  S3_STATE = OUTPUT_RESULTS.get('s3_state')
  SERVICE = DATA.get('service')
  POSITION = DATA.get('position')
  ACTIVE = DATA.get('active')
  if SERVICE.upper() == NAME.upper():
    DIR_OUTPUT = '{0}/{1:02}-{2}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper())
  else:
    DIR_OUTPUT = '{0}/{1:02}-{2}-{3}-{0}'.format(ENV.upper(), POSITION, SERVICE.upper(), NAME.upper())
  RECORDS = DATA.get('record')
  EC2_NAME = DATA.get('name')
  EC2_TYPE_INSTANCE = DATA.get('type')
  EC2_AMI = DATA.get('ami')
  EC2_AZ = DATA.get('az')
  for index, az in enumerate(['a','b','c','d','e','f']):
    if EC2_AZ == az:
      EC2_AZ = index + 1
  EC2_SSH_PORT = DATA.get('ssh_port')
  EC2_KEY_PAIR = DATA.get('key_pair')
  EC2_KEY_PAIR_NAME = EC2_KEY_PAIR.get('name')
  EC2_KEY_PAIR_PUBLIC_KEY = EC2_KEY_PAIR.get('public_key')
  EC2_SG_INGRESS = DATA.get('security_group_ingress')
  NETWORK = OUTPUT_RESULTS.get('network')
  SUBNET_PRIVATE_TOTAL = NETWORK.get('subnets_private_total')
  SUBNET_PUBLIC_TOTAL = NETWORK.get('subnets_public_total')

  results = {
    'project': PROJECT,
    'aws_account': AWS_ACCOUNT,
    'region': REGION,
    'env_upper': ENV.upper(),
    'env_lower': ENV.lower(),
    's3_state': S3_STATE,
    'service_upper': SERVICE.upper(),
    'service_lower': SERVICE.lower(),
    'position': POSITION,
    'active': ACTIVE,
    'ec2_name': EC2_NAME,
    'type_instance': EC2_TYPE_INSTANCE,
    'ami': EC2_AMI,
    'az': EC2_AZ,
    'ssh_port': EC2_SSH_PORT,
    'id_rsa_name': EC2_KEY_PAIR_NAME,
    'id_rsa_public_key': EC2_KEY_PAIR_PUBLIC_KEY
  }

  OUTPUT_SUBNETS = ''
  AZ = ['A', 'B', 'C', 'D', 'E', 'F']
  for index, subnet_private in enumerate(range(SUBNET_PRIVATE_TOTAL)):
    results_subnet_private = { 'index': index+1, 'az': AZ[subnet_private] }
    OUTPUT_SUBNETS += open('{0}/ec2/variables_subnet_private.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results_subnet_private)
  for index, subnet_public in enumerate(range(SUBNET_PUBLIC_TOTAL)):
    results_subnet_public = { 'index': index+1, 'az': AZ[subnet_public] }
    OUTPUT_SUBNETS += open('{0}/ec2/variables_subnet_public.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results_subnet_public)

  LIST_INGRESS = ''
  for sg_ingress in EC2_SG_INGRESS:
    if EC2_SG_INGRESS[sg_ingress].get('active') == True:
      for port in EC2_SG_INGRESS[sg_ingress].get('ports'):
        DESCRIPTION = EC2_SG_INGRESS[sg_ingress].get('description')
        IPV4 = EC2_SG_INGRESS[sg_ingress].get('ipv4')
        PROTOCOL = EC2_SG_INGRESS[sg_ingress].get('protocol')
        XX = {
          'description': DESCRIPTION,
          'ipv4': IPV4,
          'port': port,
          'protocol': PROTOCOL
        }
        LIST_INGRESS += open('{0}/ec2/securitygroups_ingress.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**XX)

  results['list_ingress'] = LIST_INGRESS

  TEMPLATE_EC2 = open('{0}/ec2/ec2.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_KEYS = open('{0}/ec2/keys.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER = open('{0}/ec2/provider.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_PROVIDER_S3_STATE = open('{0}/ec2/provider_s3state.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_SG = open('{0}/ec2/securitygroups.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES = open('{0}/ec2/variables.tf'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)
  TEMPLATE_VARIABLES += OUTPUT_SUBNETS
  TEMPLATE_EC2_SCRIPT_BOOTSTRAP_SH = open('{0}/ec2/script/bootstrap.sh'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

  if results.get('active') == True:
    DIR_EC2 = DIR_OUTPUT
    output_service('Serviço {1} no diretório "{0}"'.format(DIR_EC2, SERVICE.upper()))
    dirExist(DIR_EC2)

    FILE_EC2='{0}/ec2.tf'.format(DIR_EC2)
    writefile('w', FILE_EC2, TEMPLATE_EC2)

    FILE_KEYS='{0}/keys.tf'.format(DIR_EC2)
    writefile('w', FILE_KEYS, TEMPLATE_KEYS)

    if results.get('s3_state') == True:
      FILE_PROVIDER_S3_STATE='{0}/provider.tf'.format(DIR_EC2)
      writefile('w', FILE_PROVIDER_S3_STATE, TEMPLATE_PROVIDER_S3_STATE)
      
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_EC2)
      writefile('a', FILE_PROVIDER, TEMPLATE_PROVIDER)
    else:
      FILE_PROVIDER='{0}/provider.tf'.format(DIR_EC2)
      writefile('w', FILE_PROVIDER, TEMPLATE_PROVIDER)

    FILE_SG='{0}/securitygroups.tf'.format(DIR_EC2)
    writefile('w', FILE_SG, TEMPLATE_SG)

    FILE_VARIABLES='{0}/variables.tf'.format(DIR_EC2)
    writefile('w', FILE_VARIABLES, TEMPLATE_VARIABLES)

    # Create 04-EC2-DEV/script
    DIR_EC2_SCRIPT='{0}/script'.format(DIR_EC2)
    dirExist(DIR_EC2_SCRIPT)

    FILE_EC2_SCRIPT_BOOTSTRAP_SH='{0}/bootstrap.sh'.format(DIR_EC2_SCRIPT)
    writefile('w', FILE_EC2_SCRIPT_BOOTSTRAP_SH, TEMPLATE_EC2_SCRIPT_BOOTSTRAP_SH)

    TEMPLATE_SECRETS_TFVARS = open('{0}/secrets/var_ec2.tfvars'.format(DIR_TEMPLATES_AWS), 'r').read().format(**results)

    FILE_SECRETS_TFVARS='{0}/{1}/secrets.tfvars'.format(DIR, ENV.upper())
    output_service('Arquivo de Segredos "{0}"'.format(FILE_SECRETS_TFVARS))
    writefile('a', FILE_SECRETS_TFVARS, TEMPLATE_SECRETS_TFVARS)
  else:
    pass

  return results


def create_rds(DIR, FILE_YAML):
  config = yaml.safe_load(open('{0}/{1}'.format(DIR, FILE_YAML)))



def main(argv):
  CWD = '{0}'.format(os.getcwd())
  global DIR_TEMPLATES_CLOUDOPSS
  global DIR_TEMPLATES_AWS

  DIR_TEMPLATES_CLOUDOPSS = './remf'

  SCRIPT = 'REMF Scritps - IaC Terraform'
  BY = 'Roan Franklin - https://github.com/roanfranklin/'
  DATE = '06/08/2022'
  DESC = 'Script/Aplicativo para criação de ambiente com IaC - Infraestrutura como Código em Terraform.'

  parser = argparse.ArgumentParser(description='..:: {0} ::..'.format(SCRIPT))

  parser.add_argument('-f', '--file', dest='fileyaml', nargs='?', type=str, help='Seu YAML para construção do ambiente Terraform.')
  parser.add_argument('-s', '--sample', dest='samplefileyaml', action='store_true', default=False, help='Gera um YAML de exemplo.')
  parser.add_argument('-u', '--update', dest='updatesecrets', action='store_true', default=False, help='Atualiza seu "secrets.tfvars" a partir dos "terraform show".')
  parser.add_argument('-d', '--dir', dest='directory', nargs='?', type=str, default=CWD, help='Diretorio destino para criação do ambiente Terraform.')
  parser.add_argument('-t', '--templatesdir', dest='templatesdirectory', nargs='?', type=str, default=DIR_TEMPLATES_CLOUDOPSS, help='Diretorio padrão onde contém os templates Terraform.')
  parser.add_argument('-r', '--remf', dest='remf', action='store_true', default=False, help=argparse.SUPPRESS)

  args = parser.parse_args()

  DIR_TEMPLATES_AWS = '{0}/aws'.format(args.templatesdirectory)
  # DIR_TEMPLATES_GCP = '{0}/gcp'.format(args.templatesdirectory)
  # DIR_TEMPLATES_AZ = '{0}/az'.format(args.templatesdirectory)
  # DIR_TEMPLATES_OCI = '{0}/oci'.format(args.templatesdirectory)

  if args.remf is True:
    logoREMF()
    return 1

  if args.samplefileyaml is True:
    logoCloudOpss(SCRIPT, BY, DATE, DESC)
    create_yamlsample(args.directory)
    return 1

  if args.updatesecrets is True:
    logoCloudOpss(SCRIPT, BY, DATE, DESC)
    output('UPDATE', 'Atualizado o seu arquivo "secrets.tfvars" a partir dos "terraform show" de cada serviço!\n\n')
    return 1

  if not args.fileyaml is None:
    logoCloudOpss(SCRIPT, BY, DATE, DESC)
    create_secrets_tfvars(args.directory, args.fileyaml)
  else:
    logoCloudOpss(SCRIPT, BY, DATE, DESC)
    output('OPS', 'Você precisa informar um arquivo YAML. Caso tenha dúvidas verifique o HELP desse script!\n\n')
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
