import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
  os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('kibana')


# Check - Installing Kibana latest version
def test_kibana_is_installed(host):
  kibana = host.package("kibana")
  assert kibana.is_installed

# Check - Configuring Kibana
@pytest.mark.parametrize('files', [
  ("/etc/kibana/kibana.yml")
])
def test_config_kibana_exists(host, files):
  file = host.file(files)
  assert file.exists
  assert file.user == 'root'
  assert file.group == 'root'
  assert file.mode == 0o644

# Check - Service Kibana enabled, unmasked, started
def test_service_kibana_enabled_unmasked_started(host):
	kibana = host.service("kibana")
	assert kibana.is_enabled
	assert kibana.is_masked == False
	assert kibana.is_running
