# Catálogo de Tools do AI-MultiCloud-Agent

Este documento lista as tools que o AI-MultiCloud-Agent pretende suportar, começando pelo MVP de infraestrutura multi-cloud.

## Fase 1 - MVP

### Compute
- `aws_create_ec2`
- `aws_list_instances`
- `aws_stop_instance`
- `azure_create_vm`
- `azure_list_vms`
- `gcp_create_instance`
- `gcp_list_instances`
- `oci_create_instance`

### Storage
- `aws_create_s3_bucket`
- `aws_list_buckets`
- `azure_create_storage_account`
- `azure_list_containers`

### IAM (somente leitura)
- `aws_list_roles`
- `aws_get_policy`

## Expansão planejada

### Database
- `aws_create_rds_instance`
- `aws_list_rds_instances`
- `azure_create_sql_database`
- `azure_list_sql_servers`
- `gcp_create_sql_instance`
- `gcp_list_sql_instances`
- `oci_create_autonomous_database`
- `oci_list_databases`

### Networking
- `aws_create_vpc`
- `aws_list_vpcs`
- `azure_create_vnet`
- `azure_list_vnets`
- `gcp_create_vpc_network`
- `gcp_list_vpc_networks`
- `oci_create_vcn`
- `oci_list_vcns`

### Containers
- `aws_create_eks_cluster`
- `aws_list_eks_clusters`
- `azure_create_aks_cluster`
- `azure_list_aks_clusters`
- `gcp_create_gke_cluster`
- `gcp_list_gke_clusters`
- `oci_create_oke_cluster`
- `oci_list_oke_clusters`

### Serverless
- `aws_create_lambda_function`
- `aws_list_lambda_functions`
- `azure_create_function_app`
- `azure_list_function_apps`
- `gcp_create_cloud_function`
- `gcp_list_cloud_functions`

### Monitoring
- `aws_create_alarm`
- `aws_list_alarms`
- `azure_create_metric_alert`
- `azure_list_metric_alerts`
- `gcp_create_alert_policy`
- `gcp_list_alert_policies`
- `oci_create_alarm`
- `oci_list_alarms`

### Segurança
- `aws_create_security_group`
- `aws_list_security_groups`
- `azure_create_network_security_group`
- `azure_list_network_security_groups`
- `gcp_create_firewall_rule`
- `gcp_list_firewall_rules`
- `oci_create_security_list`
- `oci_list_security_lists`

## Notas adicionais

- Este catálogo deve ser mantido como referência do escopo de implementação.
- Priorizar a implementação de cada categoria em blocos pequenos e testáveis.
- Começar pelas operações de leitura e inventário antes de adicionar criação e destruição de recursos.
